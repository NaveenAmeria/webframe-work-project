from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer,     primary_key=True)
    title       = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text,        nullable=True)
    deadline    = db.Column(db.Date,        nullable=True)
    completed   = db.Column(db.Boolean,     nullable=False, default=False)
    created_at  = db.Column(db.Date,        nullable=False, default=date.today)

    def __repr__(self):
        status = 'done' if self.completed else 'pending'
        return f'<Task {self.id}: "{self.title}" [{status}]>'

    @property
    def is_overdue(self):
        """True if deadline has passed and task is not yet completed."""
        return (
            self.deadline is not None
            and not self.completed
            and self.deadline < date.today()
        )

    @property
    def is_due_today(self):
        """True if deadline is today and task is not yet completed."""
        return (
            self.deadline is not None
            and not self.completed
            and self.deadline == date.today()
        )
