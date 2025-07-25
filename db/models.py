from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ScrapedData(Base):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    url = Column(Text, unique=True)
    content = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None
        }