from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Message(db.Model):
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

    def __repr__(self):
        return f'<Massage {self.id}>'
    
    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }

    