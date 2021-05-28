from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

from .models import Task


class TaskCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title shouldn't be empty.")])

    description = TextAreaField(
        'Description',
        validators=[DataRequired(message="Description shouldn't be empty"),
                    Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")])

    priority = SelectField('Priority', choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')],
                           validators=[DataRequired(message="Priority should be set")])

    submit = SubmitField('Submit')

    def toTask(self) -> Task:
        return Task(title=self.title.data, description=self.description.data, priority=self.priority.data,
                    created=datetime.utcnow(), is_done=False)


class TaskUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message="Title shouldn't be empty.")], render_kw={'size': 31})

    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=3, max=150, message="Field must be between 3 and 150 characters long!")],
        render_kw={'cols': 35, 'rows': 5})

    priority = SelectField('Priority', choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')])

    is_done = BooleanField('Is Done')

    submit = SubmitField('Submit')

    def fromTask(self, task: Task):
        self.title.data = task.title
        self.description.data = task.description
        self.priority.data = task.priority
        self.is_done = task.is_done

        return self

    def toTask(self) -> Task:
        return Task(title=self.title.data,
                    description=self.description.data,
                    priority=self.priority.data,
                    is_done=self.is_done.data)
