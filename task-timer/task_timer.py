import os
from flask import request, Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/add", methods=["POST"])
def add_task():
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
