from flask import render_template
from __init__ import app

from cruddy.app_crud import app_crud

app.register_blueprint(app_crud)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def index():
    return render_template("about.html")


@app.route("/donate")
def index():
    return render_template("donate.html")


@app.route("/team")
def index():
    return render_template("team.html")


@app.route("/upcoming")
def index():
    return render_template("upcoming.html")


if __name__ == "__main__":
    app.run(debug=True)
