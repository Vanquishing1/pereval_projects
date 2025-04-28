-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    family_name TEXT,
    patronymic TEXT,
    phone TEXT
);

-- Таблица координат
CREATE TABLE coords (
    id SERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    height INTEGER
);

-- Таблица перевалов
CREATE TABLE pereval_added (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    coord_id INTEGER REFERENCES coords(id),
    beauty_title TEXT,
    title TEXT,
    other_titles TEXT,
    connect TEXT,
    add_time TIMESTAMP,
    winter TEXT,
    summer TEXT,
    autumn TEXT,
    spring TEXT,
    status TEXT DEFAULT 'new'
);

-- Таблица изображений
CREATE TABLE pereval_images (
    id SERIAL PRIMARY KEY,
    pereval_id INTEGER REFERENCES pereval_added(id),
    img_url TEXT
);
