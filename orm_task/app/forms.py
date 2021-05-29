from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, IntegerField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange

from orm_task.app.application import App
from .models import Task, Category, Employee, Priority

db = App().getDb()


def getPossibleCategories():
    return [(category.id, category.name) for category in Category.query.all()]


def getPossibleEmployees():
    return [(employee.id, employee.name) for employee in Employee.query.all()]


def getPossiblePriorities():
    return [(member.name, str(member.name).capitalize()) for member in Priority]


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title shouldn't be empty.")], render_kw={'size': 31})

    description = CKEditorField(
        'Description',
        validators=[DataRequired(), Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")],
        render_kw={'cols': 35, 'rows': 5})

    priority = SelectField('Priority', choices=getPossiblePriorities())

    is_done = BooleanField('Is Done')

    category_id = SelectField('Category', choices=getPossibleCategories(),
                              validators=[DataRequired(message="Category isn't present")], coerce=int)

    employees = SelectMultipleField('Employees', choices=getPossibleEmployees(), coerce=int)

    submit = SubmitField('Submit')

    def fromTask(self, task: Task):
        self.title.data = task.title
        self.description.data = task.description
        self.priority.data = task.priority.name
        self.is_done.data = task.is_done
        self.category_id.data = task.category_backref.id
        self.employees.data = [empl.id for empl in task.employee_backref]

        return self

    def toTask(self) -> Task:
        return Task(title=self.title.data,
                    description=self.description.data,
                    priority=self.priority.data,
                    category_id=db.session.query(Category.id).filter_by(id=self.category_id.data),
                    is_done=self.is_done.data)


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Category name shouldn't be empty")])

    submit = SubmitField('Submit')

    def fromCategory(self, category):
        self.name.data = category.name

    def toCategory(self):
        return Category(name=self.name.data)


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Category name shouldn't be empty")])

    count_of_completed_tasks = IntegerField('Completed tasks',
                                            validators=[NumberRange(min=0, message="Minimal possible value is zero")])

    submit = SubmitField('Submit')

    def fromEmployee(self, employee):
        self.name.data = employee.name
        self.count_of_completed_tasks.data = employee.count_of_completed_tasks

    def toEmployee(self):
        return Employee(name=self.name.data, count_of_completed_tasks=self.count_of_completed_tasks.data)
