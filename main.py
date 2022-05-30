from flask import render_template, send_from_directory
from __init__ import app

from cruddy.app_crud import app_crud
from notey.app_notes import app_notes
from contenty.app_content import app_content
from uploady.app_upload import app_upload

app.register_blueprint(app_crud)
app.register_blueprint(app_notes)
app.register_blueprint(app_content)
app.register_blueprint(app_upload)


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


@app.route("/slides")
def slides():
    return render_template("slides.html")


@app.route("/darkmode")
def darkmode():
    return render_template("darkmode.html")


@app.route("/practicequiz")
def practicequiz():
    return render_template("practicequiz.html")


@app.route("/GCAPITHF")
def GCAPITHF():
    return render_template("GoogleCalendarAPI_test_html_file.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# serve uploaded files so they can be downloaded by users.
@app.route('/uploads/<name>')
def uploads_endpoint(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# register "uploads_endpoint" endpoint so url_for will find all uploaded files
app.add_url_rule(
    "/" + app.config['UPLOAD_FOLDER'] + "/<name>", endpoint="uploads_endpoint", build_only=True
)

if __name__ == "__main__":
    app.run(debug=True)
