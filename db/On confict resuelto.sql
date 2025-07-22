ALTER TABLE scraped_data
ADD CONSTRAINT unique_url UNIQUE (url);

SELECT id, title, url, content, scraped_at
FROM scraped_data
WHERE url = 'https://prueba.com/documento.pdf';

SELECT * FROM scraped_data
ORDER BY scraped_at DESC
LIMIT 5;