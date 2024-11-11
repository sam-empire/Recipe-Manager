CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    instructions TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    image_url TEXT,
    category TEXT
);
