-- Таблица ролей пользователей
CREATE TABLE users_roles (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL
);

-- Таблица классов
CREATE TABLE classes (
    id serial PRIMARY KEY,
    number integer,
    letter varchar(255),
    year integer NOT NULL,
    is_active boolean NOT NULL,
    class_rate integer NOT NULL
);

-- Таблица пользователей
CREATE TABLE users (
    id serial PRIMARY KEY,
    name varchar(255),
    lastname varchar(255),
    patronymic varchar(255) NOT NULL,
    age integer NOT NULL,
    class_id integer NOT NULL,
    phone_number varchar(50) NOT NULL,
    email varchar(255) NOT NULL,
    created_at date NOT NULL,
    avatar_url text NOT NULL,
    user_rate integer NOT NULL,
    role_id integer NOT NULL,
    is_complex boolean NOT NULL,
    CONSTRAINT users_fk_class FOREIGN KEY (class_id) REFERENCES classes(id),
    CONSTRAINT users_fk_role FOREIGN KEY (role_id) REFERENCES users_roles(id),
    CONSTRAINT users_email_unique UNIQUE (email)
);

-- Таблица для связи "друзья" (многие-ко-многим)
CREATE TABLE user_friends (
    user_id integer NOT NULL,
    friend_id integer NOT NULL,
    PRIMARY KEY (user_id, friend_id),
    CONSTRAINT user_friends_fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT user_friends_fk_friend FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT user_friends_check CHECK (user_id != friend_id)
);

-- Таблица типов продуктов
CREATE TABLE product_types (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL
);

-- Таблица продуктов
CREATE TABLE products (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    blc integer NOT NULL,
    mass integer NOT NULL,
    rate integer NOT NULL,
    picture_url varchar(255) NOT NULL,
    price float NOT NULL,
    compound text NOT NULL,
    is_hidden boolean NOT NULL,
    is_complex boolean NOT NULL,
    product_type_id integer NOT NULL,
    CONSTRAINT products_fk_type FOREIGN KEY (product_type_id) REFERENCES product_types(id)
);

-- Таблица статусов заказов
CREATE TABLE order_statuses (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL
);

-- Таблица заказов
CREATE TABLE orders (
    id serial PRIMARY KEY,
    order_name varchar(255) NOT NULL,
    user_id integer NOT NULL,
    product_id integer NOT NULL,
    created_at timestamp NOT NULL,
    status_id integer NOT NULL,
    CONSTRAINT orders_fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT orders_fk_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT orders_fk_status FOREIGN KEY (status_id) REFERENCES order_statuses(id)
);

-- Таблица отзывов
CREATE TABLE reviews (
    id serial PRIMARY KEY,
    user_id integer NOT NULL,
    message varchar(255) NOT NULL,
    created_at timestamp NOT NULL,
    picture_url text NOT NULL,
    is_support boolean NOT NULL,
    CONSTRAINT reviews_fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Таблица комплексов
CREATE TABLE complexes (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    creation_date date NOT NULL,
    is_closed boolean NOT NULL
);

-- Таблица для связи пользователей и комплексов (многие-ко-многим)
CREATE TABLE user_complexes (
    user_id integer NOT NULL,
    complex_id integer NOT NULL,
    PRIMARY KEY (user_id, complex_id),
    CONSTRAINT user_complexes_fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT user_complexes_fk_complex FOREIGN KEY (complex_id) REFERENCES complexes(id) ON DELETE CASCADE
);

-- Таблица для связи комплексов и продуктов (многие-ко-многим)
CREATE TABLE complex_products (
    complex_id integer NOT NULL,
    product_id integer NOT NULL,
    PRIMARY KEY (complex_id, product_id),
    CONSTRAINT complex_products_fk_complex FOREIGN KEY (complex_id) REFERENCES complexes(id) ON DELETE CASCADE,
    CONSTRAINT complex_products_fk_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Таблица дней недели (справочник)
CREATE TABLE weekdays (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE
);

-- Заполнение таблицы дней недели
INSERT INTO weekdays (name) VALUES
    ('Monday'),
    ('Tuesday'),
    ('Wednesday'),
    ('Thursday'),
    ('Friday'),
    ('Saturday'),
    ('Sunday');

-- Таблица для связи комплексов и дней недели (многие-ко-многим)
CREATE TABLE complex_weekdays (
    complex_id integer NOT NULL,
    weekday_id integer NOT NULL,
    PRIMARY KEY (complex_id, weekday_id),
    CONSTRAINT complex_weekdays_fk_complex FOREIGN KEY (complex_id) REFERENCES complexes(id) ON DELETE CASCADE,
    CONSTRAINT complex_weekdays_fk_weekday FOREIGN KEY (weekday_id) REFERENCES weekdays(id) ON DELETE RESTRICT
);

-- Индексы для оптимизации запросов
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_complex_weekdays_complex_id ON complex_weekdays(complex_id);
CREATE INDEX idx_complex_weekdays_weekday_id ON complex_weekdays(weekday_id);