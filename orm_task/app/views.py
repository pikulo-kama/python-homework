from flask import render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm

from .application import App
from .forms import TaskCreateForm, TaskUpdateForm
from .models import Task

app = App().getApp()


@app.route('/task', methods=['GET'])
def find_all():
    return render_template('task/index.html', title="Tasks", tasks=Task.query.all())


@app.route('/task/<taskId>', methods=['GET'])
def find_by_id(taskId: int):
    task = Task.findById(taskId)

    if task is None:
        flash('Task not found', category='error')
        return redirect(url_for('find_all'))

    return render_template('task/show.html', title=task.title, task=task, form=FlaskForm())


@app.route('/task/create', methods=['GET', 'POST'])
def create():
    form = TaskCreateForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            if form.toTask().save():
                return redirect(url_for('find_all'))

        flash("Invalid data", category='error')

    return render_template('task/create.html', title='Create task', form=form)


@app.route('/task/<taskId>/update', methods=['GET', 'POST'])
def update(taskId: int):
    form = TaskUpdateForm()
    task = Task.findById(taskId)

    if request.method == 'GET':

        if task:
            form.fromTask(task)

    elif request.method == 'POST':

        if form.validate_on_submit():

            if task.update(form):
                return redirect(url_for('find_by_id', id=taskId))

        flash("Invalid data", category='error')

    return render_template('task/update.html', id=taskId, title=f"Update task {taskId}", form=form)


@app.route('/task/<taskId>/delete', methods=['GET', 'POST'])
def delete(taskId: int):
    if Task.deleteById(taskId):
        flash("Task was deleted", category='info')
        return redirect(url_for('find_all'))

    else:
        flash("Task wasn't deleted", category='error')
        return redirect(url_for('find_by_id', id=taskId))
