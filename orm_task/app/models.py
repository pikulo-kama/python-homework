from enum import Enum

from flask import flash

from .application import App

app = App().getApp()
db = App().getDb()


class Priority(Enum):
    LOW = 1,
    MEDIUM = 2,
    HIGH = 3


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.VARCHAR(255), nullable=False)

    description = db.Column(db.VARCHAR(255), nullable=False)

    created = db.Column(db.TIMESTAMP())

    priority = db.Column(db.Enum(Priority), default=Priority.LOW)

    is_done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f'<Task {self.id} {self.title} {self.description} {self.created} {self.priority} {self.is_done}>'

    def update(self, form) -> bool:
        try:
            self.title = form.title.data
            self.description = form.description.data
            self.priority = form.priority.data
            self.is_done = form.is_done.data

            db.session.commit()
            return True

        except Exception as e:
            print(e)

            db.session.rollback()

        return False

    def save(self) -> bool:
        try:
            db.session.add(self)
            db.session.commit()
            flash('Task successfully created', category='info')
            return True

        except Exception as e:

            print(e)

            db.session.rollback()
            flash("Server error occurred. Task wasn't stored")

            return False

    @classmethod
    def findById(cls, taskId: int):
        try:
            return cls.query.get(taskId)

        except Exception as e:
            print(e)
            return None

    @classmethod
    def deleteById(cls, taskId: int) -> bool:
        task = Task.query.get_or_404(taskId)

        try:
            db.session.delete(task)
            db.session.commit()

            return True
        except Exception as e:

            print(e)

            db.session.rollback()

        return False
