from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app instance.
app = Flask(__name__)

# Configure the database environment variables for the app instance.
# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Instantiate the database.
db = SQLAlchemy(app)

# Create a model class for the todo items.
class Todo(db.Model):
    # Each todo item has a primary key integer.
    id = db.Column(db.Integer, primary_key=True)
    # Each todo item has a string title
    # with a max of 100 characters.
    title = db.Column(db.String(100))
    # Each todo item has a completed boolean flag.
    complete = db.Column(db.Boolean)

# Need the app context when creating the database.
# Reference: https://stackoverflow.com/a/60879370
with app.app_context():
    # Create the database before running the app.
    db.create_all()

# Execute the home() function upon navigation to http://localhost:5000/
@app.route("/")
def home():
    # Get a list of Todo instances from the database.
    todo_list = Todo.query.all()
    # Render the base.html template and pass the todo list,
    # so that each item can be rendered using the templating lanuage.
    return render_template("base.html", todo_list=todo_list)

# Execute the add() function upon a POST request to http://localhost:5000/add
# which will be made by the <form/> element in the home page.
@app.route("/add", methods=["POST"])
def add():
    # Get the name of the new task from the form body.
    title = request.form.get("title")
    # Create a new Todo model instance, and pass the task name as the title.
    new_todo = Todo(title=title, complete=False)
    # Add the new Todo task to the database.
    db.session.add(new_todo)
    # Commit the transaction to actually do the addition.
    db.session.commit()
    # Redirect the user back to the main todo list page.
    return redirect(url_for("home"))

# Execute the update() function upon a GET request to http://localhost:5000/update/{todo_id}
# where {todo_id} is the primary key of the task to update (toggle its completion status).
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Find the todo instance of interest based on the ID from the URL.
    todo = Todo.query.filter_by(id=todo_id).first()
    # Toggle the completion status flag.
    todo.complete = not todo.complete
    # Commit the update to the database.
    db.session.commit()
    # Redirect the user back to the main todo list page.
    return redirect(url_for("home"))

# Execute the delete() function upon a GET request to http://localhost:5000/delete/{todo_id}
# where {todo_id} is the primary key of the task to delete from the database.
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Find the todo instance of interest based on the ID from the URL.
    todo = Todo.query.filter_by(id=todo_id).first()
    # Delete the task from the database.
    db.session.delete(todo)
    # Commit the deletion to the database.
    db.session.commit()
    # Redirect the user back to the main todo list page.
    return redirect(url_for("home"))

# Run the following code when the script is invoked
# from the command line.
if __name__ == "__main__":
    # Start the flask web server,
    # so that it can listen on the routes defined above.
    app.run(debug=True)