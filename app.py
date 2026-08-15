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
        if request.form.get("completed"):
            task_id = request.form.get("id")
            db = sqlite3.connect("todo.db")
            db.execute("UPDATE todos SET completed = 1 WHERE id = ?", (task_id,))
            db.commit()
            db.close()
            return redirect("/")
        task = request.form.get("newtask")
        
        if task:
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

