from datetime import datetime
import os
from pprint import pp
import sqlalchemy as sa
from flask import request, Flask, url_for, redirect, render_template, jsonify, flash
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super secret key'
# MySql Config
# app.config["MYSQL_DATABASE_USER"] = os.getenv("db_user")  # from app-configs.yml
# app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")  # from app-secrets.yml
# app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")  # from app-configs.yml
# app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
# app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
# # mysql://username:password@host:port/database_name
# uri = f'{os.getenv("db_user")}:{os.getenv("db_root_password")}@{os.getenv("MYSQL_SERVICE_HOST")}:{int(os.getenv("MYSQL_SERVICE_PORT"))}/{os.getenv("db_name")}'
uri = "root:localpass@localhost:50238/todoapp"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{uri}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app_data = {
    "name": "ToDo List Web App",
    "description": "A basic todo app",
    "author": "Saurabh Chatterjee",
    "html_title": "TodoApp",
    "project_name": "ToDo App",
    "keywords": "flask, webapp, template, basic",
}


class Tasks(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    task_name = sa.Column(sa.String(255), unique=False, nullable=False)
    task_details = sa.Column(sa.String(255), unique=False)
    started_on = sa.Column(sa.TIMESTAMP, unique=False, nullable=False)
    completed_on = sa.Column(sa.TIMESTAMP, unique=False)
    due_on = sa.Column(sa.TIMESTAMP, unique=False)
    is_completed = sa.Column(sa.Boolean, unique=False, default=True)

    def __init__(self, task_name, task_details, started_on):
        self.task_name = task_name
        self.task_details = task_details
        self.started_on = started_on


@app.route("/")
def index():
    db.create_all()
    return render_template('index.html', app_data=app_data)


@app.route("/tasks/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == 'POST':
        form_data_raw = request.form
        form_data_json = dict(form_data_raw)
        print(form_data_json)
        task_name = form_data_json['taskName']
        task_details = form_data_json['taskDetails']
        started_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(started_on)
        task = Tasks(task_name=task_name, task_details=task_details, started_on=started_on)
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!")
        return redirect(url_for('index', app_data=app_data))
    return render_template('add_task.html', app_data=app_data)


@app.route("/tasks/view_tasks", methods=["GET"])
def view_all_tasks():
    data = db.session.query(Tasks).all()
    results = {}
    for d in data:
        is_completed = 'True' if d.is_completed else 'False'
        today = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        end_date = today if not d.completed_on else d.completed_on
        time_spent_hours = round((end_date - d.started_on).total_seconds() / 3600)

        results[d.id] = {'name': d.task_name,
                         'details': d.task_details,
                         'started_on': d.started_on.strftime('%Y-%m-%d %H:%M:%S'),
                         'completed_on': end_date.strftime('%Y-%m-%d %H:%M:%S'),
                         'time_spent': f'{time_spent_hours} hrs.'
                         }
    pp(f"results are: {results}")
    return render_template('view_task.html', tasks=results, app_data=app_data)


@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == 'POST':
        form_data_raw = request.form
        form_data_json = dict(form_data_raw)
        task_name = form_data_json['taskName']
        task_details = form_data_json['taskDetails']
        data = db.session.query(Tasks).filter_by(id=task_id).first()
        data.task_name = task_name
        data.task_details = task_details
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('view_all_tasks', app_data=app_data))
    data = db.session.query(Tasks).filter_by(id=task_id).first()
    print(f"{data.task_name}, {data.task_details}, {data.id}")
    return render_template('edit_task.html', output=[task_id, data.task_name, data.task_details])


@app.route("/tasks/mark_complete/<int:task_id>", methods=["GET", "POST"])
def mark_complete(task_id):
    data = db.session.query(Tasks).filter_by(id=task_id).first()
    data.completed_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.is_completed = True
    db.session.add(data)
    db.session.commit()
    flash("task completed successfully")
    return redirect(url_for('view_all_tasks', app_data=app_data))


@app.route("/tasks/delete/<int:task_id>")
def delete_task(task_id):
    data = db.session.query(Tasks).filter_by(id=task_id).first()
    db.session.delete(data)
    db.session.commit()
    flash("task deleted")
    return redirect(url_for('view_all_tasks', app_data=app_data))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3003)
