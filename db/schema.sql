CREATE TABLE scraped_data (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT,
    content TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM scraped_data;