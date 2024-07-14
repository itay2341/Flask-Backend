from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Message(db.Model):
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now())
    
    def save(self):
        """
        Save message to database.
        """
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all_messages_sorted_by_created_time():
        """
        Get all messages sorted by created time.
        """
        messages = Message.query.order_by(Message.created_at).all()
        return [{"role": message.role, "content": message.content} for message in messages]


    