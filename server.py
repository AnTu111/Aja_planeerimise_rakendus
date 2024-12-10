from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Хранилище задач
tasks = {"ongoing": [], "completed": []}

@app.route("/")
def index():
    check_deadlines()  # Проверка дедлайнов перед загрузкой страницы
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    deadline_date = request.form.get("deadline_date")
    deadline_time = request.form.get("deadline_time")
    if title and deadline_date and deadline_time:
        try:
            # Объединяем дату и время
            deadline = datetime.strptime(f"{deadline_date} {deadline_time}", "%Y-%m-%d %H:%M")
            tasks["ongoing"].append({
                "title": title,
                "deadline": deadline,
                "added_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except ValueError:
            pass  # Игнорируем ошибки в формате даты/времени
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = tasks["ongoing"].pop(task_id)
    tasks["completed"].append(task)
    return redirect(url_for("index"))

@app.route("/delete/<string:section>/<int:task_id>")
def delete_task(section, task_id):
    if section in tasks and 0 <= task_id < len(tasks[section]):
        tasks[section].pop(task_id)
    return redirect(url_for("index"))

def check_deadlines():
    """Проверяет дедлайны задач в ongoing и переносит просроченные в completed."""
    current_time = datetime.now()
    for task in list(tasks["ongoing"]):  # Копируем список для безопасного удаления
        if task["deadline"] <= current_time:
            tasks["ongoing"].remove(task)
            tasks["completed"].append({
                "title": task["title"],
                "deadline": task["deadline"],
                "completed_time": current_time.strftime("%Y-%m-%d %H:%M:%S")
            })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
