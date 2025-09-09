from io import BytesIO
from datetime import date, timedelta
from collections import defaultdict

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin
from app.models.users import User, Class
from app.models.complexes import UserComplexChoice, Complex, Weekday


router = APIRouter(prefix="/exports", tags=["exports"]) 


def _current_monday(today: date) -> date:
    return today - timedelta(days=today.weekday())


def _last_week_monday(today: date) -> date:
    return _current_monday(today) - timedelta(days=7)


def _next_monday(today: date) -> date:
    return today + timedelta(days=((7 - today.weekday()) % 7))


def _resolve_week_start(db: Session, mode: str | None, explicit: date | None) -> date:
    """
    Resolve which week_start to export:
    - if explicit provided -> use it
    - if mode == 'last' -> last completed week's Monday
    - if mode == 'current' -> current week's Monday
    - if mode == 'next' -> next Monday
    - else (None or 'latest') -> latest available week_start in user_complex_choices
    """
    today = date.today()
    if explicit:
        return explicit
    if mode == "last":
        return _last_week_monday(today)
    if mode == "current":
        return _current_monday(today)
    if mode == "next":
        return _next_monday(today)

    # latest by data
    latest = db.execute(
        select(UserComplexChoice.week_start)
        .distinct()
        .order_by(UserComplexChoice.week_start.desc())
        .limit(1)
    ).scalar_one_or_none()
    return latest or _last_week_monday(today)


@router.get(
    "/choices/last-week.xlsx",
    description=(
        "Экспорт выборов комплексов. По умолчанию — последняя доступная неделя по данным. "
        "Можно указать ?week=last|current|next|latest и/или ?week_start=YYYY-MM-DD"
    )
)
def export_last_week_choices(
    db: Session = Depends(db_session),
    week: str | None = None,
    week_start: date | None = None,
):
    # Determine target week start
    target_week_start = _resolve_week_start(db, week, week_start)

    # Fetch choices joined with users, classes, weekdays, complexes
    stmt = (
        select(
            Class.id.label("class_id"),
            Class.number,
            Class.letter,
            User.id.label("user_id"),
            User.lastname,
            User.name,
            User.patronymic,
            Weekday.id.label("weekday_id"),
            Weekday.name.label("weekday_name"),
            Complex.name.label("complex_name"),
        )
        .join(User, User.class_id == Class.id)
        .join(UserComplexChoice, UserComplexChoice.user_id == User.id)
        .join(Weekday, Weekday.id == UserComplexChoice.weekday_id)
        .join(Complex, Complex.id == UserComplexChoice.complex_id)
        .where(UserComplexChoice.week_start == target_week_start)
        .order_by(Class.id, User.lastname, User.name, Weekday.id)
    )

    rows = db.execute(stmt).all()

    # Group rows by class
    by_class: dict[int, list] = defaultdict(list)
    class_titles: dict[int, str] = {}
    for r in rows:
        cls_id = r.class_id
        class_titles[cls_id] = f"{r.number or ''}{(r.letter or '').strip()}".strip() or f"class_{cls_id}"
        by_class[cls_id].append(r)

    # Create workbook with openpyxl
    try:
        from openpyxl import Workbook
    except ImportError:  # pragma: no cover
        raise RuntimeError("openpyxl is required for export. Please add it to requirements and install.")

    wb = Workbook()
    # Remove default sheet; we'll add per-class
    default_sheet = wb.active
    wb.remove(default_sheet)

    # If no data, still provide an empty workbook with a note
    if not by_class:
        ws = wb.create_sheet("No data")
        ws.append(["Нет данных за неделю", str(target_week_start)])
    else:
        for cls_id, items in by_class.items():
            title = class_titles.get(cls_id, f"class_{cls_id}")
            # Excel sheet title max 31 chars and cannot contain certain characters
            safe_title = title[:31].replace("/", "-").replace("\\", "-").replace("*", "-").replace("[", "(").replace("]", ")").replace(":", "-")
            ws = wb.create_sheet(safe_title or f"class_{cls_id}")

            # Header
            ws.append([
                "Фамилия",
                "Имя",
                "Отчество",
                "День недели",
                "Комплекс",
            ])

            for r in items:
                ws.append([
                    r.lastname,
                    r.name,
                    r.patronymic,
                    r.weekday_name,
                    r.complex_name,
                ])

    # Save to bytes
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)

    filename = f"choices_{target_week_start.isoformat()}.xlsx"
    headers = {
        "Content-Disposition": f"attachment; filename=\"{filename}\""
    }
    return Response(
        content=buf.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
