from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from sqlalchemy import case, desc

from .application import App
from .forms import TaskForm, CategoryForm, EmployeeForm, getPossiblePriorities
from .models import Task, Category, Employee

app = App().getApp()


@app.route('/task', methods=['GET'])
def task_find_all():
    tasks = Task.query.order_by(desc(case(value=Task.priority, whens={'LOW': 1, 'MEDIUM': 2, 'HIGH': 3})),
                                Task.created.desc()).all()
    categories = {category.id: category.name for category in Category.query.all()}

    return render_template('task/index.html',
                           title="Tasks",
                           tasks=tasks,
                           categories=categories)


@app.route('/task/<taskId>', methods=['GET'])
def task_find_by_id(taskId: int):
    task = Task.findById(taskId)

    if task is None:
        flash('Task not found', category='error')
        return redirect(url_for('task_find_all'))

    return render_template('task/show.html', title=task.title, task=task, form=FlaskForm())


@app.route('/task/create', methods=['GET', 'POST'])
def task_create():
    form = TaskForm()

    if request.method == 'POST':

        if form.is_submitted():

            form.is_done.data = False
            form.validate()

            task = form.toTask()
            task.created = datetime.utcnow()

            if task.save():
                return redirect(url_for('task_find_all'))

        flash("Invalid data", category='error')

    return render_template('task/form.html',
                           title='Create task',
                           form=form,
                           endpoint='task_create',
                           categories=Category.query.all(),
                           priorities=getPossiblePriorities(),
                           employees=Employee.query.all())


@app.route('/task/<taskId>/update', methods=['GET', 'POST'])
def task_update(taskId: int):
    form = TaskForm()
    task = Task.findById(taskId)

    if request.method == 'GET':

        if task:
            form.fromTask(task)

    elif request.method == 'POST':

        if form.is_submitted():

            form.validate()

            task.created = datetime.utcnow()

            if task.update(form):
                return redirect(url_for('task_find_by_id', taskId=taskId))

        else:
            flash("Invalid data", category='error')

    return render_template('task/form.html',
                           id=taskId,
                           title=f"Update task {taskId}",
                           endpoint='task_update',
                           form=form,
                           categories=Category.query.all(),
                           priorities=getPossiblePriorities(),
                           employees=Employee.query.all())


@app.route('/task/<taskId>/delete', methods=['GET', 'POST'])
def task_delete(taskId: int):
    if Task.deleteById(taskId):
        flash("Task was deleted", category='info')
        return redirect(url_for('task_find_all'))

    else:
        flash("Task wasn't deleted", category='error')
        return redirect(url_for('task_find_by_id', taskId=taskId))


@app.route('/category', methods=['GET'])
def category_find_all():
    return render_template('category/index.html', title="Categories", categories=Category.query.all())


@app.route('/category/<categoryId>', methods=['GET'])
def category_find_by_id(categoryId: int):
    category = Category.findById(categoryId)

    if category is None:
        flash('Category not found', category='error')
        return redirect(url_for('category_find_all'))

    return render_template('category/show.html',
                           title=category.name,
                           tasks=Task.query.filter_by(category_id=categoryId),
                           category=category,
                           form=FlaskForm())


@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    form = CategoryForm()

    if request.method == 'POST':
        print('ok')
        if form.validate_on_submit():

            if not Category.existsByName(form.name.data):

                if form.toCategory().save():
                    return redirect(url_for('category_find_all'))

    return render_template('category/form.html', endpoint='category_create', title='Create category', form=form)


@app.route('/category/<categoryId>/update', methods=['GET', 'POST'])
def category_update(categoryId: int):
    form = CategoryForm()
    category = Category.findById(categoryId)

    if request.method == 'GET':

        if category:
            form.fromCategory(category)

    elif request.method == 'POST':
        if form.validate_on_submit():

            if not Category.existsByName(form.name.data):
                if category.update(form):
                    return redirect(url_for('category_find_by_id', categoryId=categoryId))

            flash("Category with this name already exists", category='error')

    return render_template('category/form.html', id=category.id, endpoint='category_update',
                           title=f"Update category {category.name}", form=form)


@app.route('/category/<categoryId>/delete', methods=['GET', 'POST'])
def category_delete(categoryId: int):
    if Category.deleteById(categoryId):
        flash("Category was deleted", category='info')
        return redirect(url_for('category_find_all'))

    else:
        flash("Category wasn't deleted", category='error')
        return redirect(url_for('category_find_by_id', categoryId=categoryId))


@app.route('/employee', methods=['GET'])
def employee_find_all():
    return render_template('employee/index.html',
                           title="Employees",
                           employees=Employee.query.all(),
                           )


@app.route('/employee/<employeeId>', methods=['GET'])
def employee_find_by_id(employeeId: int):
    employee = Employee.findById(employeeId)

    if employee is None:
        flash('Employee not found', category='error')
        return redirect(url_for('task_find_all'))

    tasks = employee.tasks()

    completed = len(list(filter(lambda task: task.is_done, tasks.all())))
    uncompleted = len(tasks.all()) - completed

    return render_template('employee/show.html',
                           title=employee.name,
                           employee=employee,
                           tasks=tasks,
                           completed=completed,
                           uncompleted=uncompleted,
                           form=FlaskForm())


@app.route('/employee/create', methods=['GET', 'POST'])
def employee_create():
    form = EmployeeForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            form.count_of_completed_tasks.data = 0

            if form.toEmployee().save():
                return redirect(url_for('employee_find_all'))

    return render_template('employee/form.html', endpoint='employee_create', title='Add employee', form=form)


@app.route('/employee/<employeeId>/update', methods=['GET', 'POST'])
def employee_update(employeeId: int):
    form = EmployeeForm()
    employee = Employee.findById(employeeId)

    if request.method == 'GET':

        if employee:
            form.fromEmployee(employee)

    elif request.method == 'POST':
        if form.validate_on_submit():

            if employee.update(form):
                return redirect(url_for('employee_find_by_id', employeeId=employeeId))

            flash("Employee with this name already exists", employee='error')

    return render_template('employee/form.html', id=employee.id, endpoint='employee_update',
                           title=f"Update {employee.name} info", form=form)


@app.route('/employee/<employeeId>/delete', methods=['GET', 'POST'])
def employee_delete(employeeId: int):
    if Employee.deleteById(employeeId):
        flash("Employee was deleted", category='info')
        return redirect(url_for('employee_find_all'))

    else:
        flash("Employee wasn't deleted", category='error')
        return redirect(url_for('employee_find_by_id', employeeId=employeeId))
