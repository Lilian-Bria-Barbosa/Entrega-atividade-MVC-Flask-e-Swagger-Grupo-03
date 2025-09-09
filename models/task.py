from models import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Task(db.Model):
    __tablename__ = "tasks"  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="Pendente") 

    user = db.relationship("User", back_populates="tasks")

    def to_dict(self, include_user = False):
        data = {
            "id": self.id, 
            "title": self.title,
            "description": self.description, 
            "status": self.status, 
            "user_id": self.user_id, 
        }
        if include_user and self.user:
            data["user_name"] = self.user.name 

            
    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"
