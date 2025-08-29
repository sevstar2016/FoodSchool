from fastapi import FastAPI, APIRouter
from app.api import users as users_router
from app.api import products as products_router
from app.api import complexes as complexes_router
from app.api import orders as orders_router
from app.api import auth as auth_router
from app.api import classes as classes_router


def create_app() -> FastAPI:
    app = FastAPI(title="FoodAPI", version="0.1.0", docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")

    api = APIRouter(prefix="/api")

    @api.get("/health")
    def healthcheck():
        return {"status": "ok"}

    api.include_router(users_router.router)
    api.include_router(products_router.router)
    api.include_router(complexes_router.router)
    api.include_router(orders_router.router)
    api.include_router(auth_router.router)
    api.include_router(classes_router.router)

    app.include_router(api)

    return app


app = create_app()


