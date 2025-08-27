from models import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Task(db.Model):
    __tablename__ = "tasks"  # CORRIGIDO

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="Pendente")  # já está correto

    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"
