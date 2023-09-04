import os
from flask import request, Flask, url_for, redirect, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
# mysql = MySQL()
#
# # MySql Config
# app.config["MYSQL_DATABASE_USER"] = "root"
# app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
# app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
# app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
# app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
# mysql.init_app(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return "add new tasks here"


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    return "get all tasks here"


@app.route("/task/<int:task_id>", methods=["GET"])
def get_task(task_id):
    return f"get details for task id {task_id} here"


@app.route("/task/update/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    return f"update task id {task_id} here"


@app.route("/task/start/<int:task_id>", methods=["GET", "POST"])
def start_task(task_id):
    return f"start task id {task_id} here"


@app.route("/task/pause/<int:task_id>", methods=["GET", "POST"])
def pause_task(task_id):
    return f"pause task id {task_id} here"


@app.route("/task/stop/<int:task_id>", methods=["GET", "POST"])
def stop_task(task_id):
    return f"stop task id {task_id} here"


@app.route("/task/delete/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    return f"delete task id {task_id} here"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3003)
