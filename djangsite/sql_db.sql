CREATE TABLE IF NOT EXISTS uploaded_photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    predicted_class TEXT NOT NULL,
    upload_time DATETIME NOT NULL
);
