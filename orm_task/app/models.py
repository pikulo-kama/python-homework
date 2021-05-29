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

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return f'<Task {self.id} {self.title} {self.description} {self.created} {self.priority} {self.is_done} {self.category_id}>'

    def update(self, form) -> bool:
        try:
            self.title = form.title.data
            self.description = form.description.data
            self.priority = form.priority.data
            self.is_done = form.is_done.data
            self.category_id = db.session.query(Category.id).filter(Category.id == form.category_id.data)

            self.employee_backref.clear()

            was_done = db.session.query(Task).with_entities(Task.is_done).filter_by(id=self.id).first()[0]

            for employeeId in form.employees.data:

                print('call')
                employee = Employee.query.get_or_404(employeeId)

                if was_done and not self.is_done:
                    employee.count_of_completed_tasks -= 1

                elif not was_done and self.is_done:
                    employee.count_of_completed_tasks += 1

                self.employee_backref.append(employee)

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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)

    category = db.relationship('Task', backref='category_backref', lazy=True)

    @classmethod
    def existsByName(cls, name: str):

        if db.session.query(Category).filter_by(name=name).first() is not None:
            flash('Category with this name already exists.', category='error')
            return True

        return False

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            flash('Category successfully created', category='info')
            return True

        except Exception as e:

            print(e)

            db.session.rollback()
            flash("Server error occurred. Category wasn't stored")

            return False

    @classmethod
    def findById(cls, categoryId: int):
        try:
            return cls.query.get(categoryId)

        except Exception as e:
            print(e)
            return None

    def update(self, form) -> bool:
        try:
            self.name = form.name.data

            db.session.commit()
            return True

        except Exception as e:
            print(e)

            db.session.rollback()

        return False

    @classmethod
    def deleteById(cls, categoryId: int) -> bool:
        category = Category.query.get_or_404(categoryId)

        try:
            db.session.delete(category)
            db.session.commit()

            return True
        except Exception as e:
            print(e)

            db.session.rollback()

        return False

    def __repr__(self):
        return f'<Category {self.id} {self.name}>'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)

    count_of_completed_tasks = db.Column(db.Integer)

    task_empl = db.relationship('Task', secondary=db.Table('task_empl',
                                                           db.Column('employee_id', db.Integer,
                                                                     db.ForeignKey('employee.id')),
                                                           db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                                                           ), backref=db.backref('employee_backref'))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            flash('Employee successfully created', category='info')
            return True

        except Exception as e:

            print(e)

            db.session.rollback()
            flash("Server error occurred. Employee wasn't stored")

            return False

    @classmethod
    def findById(cls, employeeId: int):
        try:
            return cls.query.get(employeeId)

        except Exception as e:
            print(e)
            return None

    def update(self, form) -> bool:
        try:
            self.name = form.name.data
            self.count_of_completed_tasks = form.count_of_completed_tasks.data

            db.session.commit()
            return True

        except Exception as e:
            print(e)

            db.session.rollback()

        return False

    @classmethod
    def deleteById(cls, employeeId: int) -> bool:
        employee = Employee.query.get_or_404(employeeId)

        try:
            db.session.delete(employee)
            db.session.commit()

            return True
        except Exception as e:
            print(e)

            db.session.rollback()

        return False

    def tasks(self):
        return db.session.query(Task).filter(Task.employee_backref.contains(self))

    def __repr__(self):
        return f'<Employee {self.id} {self.name} {self.count_of_completed_tasks}>'
