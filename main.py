from flask import render_template
from __init__ import app

from cruddy.app_crud import app_crud
from notey.app_notes import app_notes

app.register_blueprint(app_crud)
app.register_blueprint(app_notes)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/donate")
def donate():
    return render_template("donate.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/upcoming")
def upcoming():
    return render_template("upcoming.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
