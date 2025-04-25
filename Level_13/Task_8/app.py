from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/add",methods=["POST"])
def add():
    todo_text=request.form['todo']
    new_todo=Todo(task=todo_text)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo=Todo.query.get_or_404(id)
    if request.method == "POST":
        todo.task = request.form["todo"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)

@app.route("/check/<int:id>")
def check(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)