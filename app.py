import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
def init_db():
    db = sqlite3.connect("todo.db")

    db.execute("""CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE
    )""")

    db.commit()
    db.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("action") == "update":
            task_id = request.form.get("id")

            db = sqlite3.connect("todo.db")
            
            task = db.execute("SELECT completed FROM todos WHERE id = ?", (task_id,)).fetchone()

            new_status = 0 if task[0] == 1 else 1

            db.execute("UPDATE todos SET completed = ? WHERE id = ?", (new_status, task_id))

            db.commit()
            db.close()

            return redirect("/")
        if request.form.get("action") == "delete":
            task_id = request.form.get("id")

            db = sqlite3.connect("todo.db")
            db.execute("DELETE FROM todos WHERE id = ?", (task_id,))
            db.commit()
            db.close()

            return redirect("/")
        if request.form.get("action") == "edit":
            task_id = request.form.get("id")
            new_title = request.form.get("title")
            if not new_title:
                return redirect("/")
            db = sqlite3.connect("todo.db")
            db.execute("UPDATE todos SET title = ? WHERE id = ?", (new_title, task_id))
            db.commit()
            db.close()

            return redirect("/")
        else:
            task = request.form.get("newtask")
            if not task:
                return redirect("/")
            db = sqlite3.connect("todo.db")
            db.execute("INSERT INTO todos (title) VALUES (?)", (task,))
            db.commit()
            db.close()
            return redirect("/")

    else:
        db = sqlite3.connect("todo.db")
        db.row_factory = sqlite3.Row

        tasks = db.execute("SELECT * FROM todos").fetchall()
        db.close()

        return render_template("index.html", tasks=tasks)

