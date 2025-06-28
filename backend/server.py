import flask
from os import path
from engine import util


app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.redirect("/index.html")


@app.route("/<path:page>")
def showPage(page):
    return flask.send_from_directory(path.join(util.cwd, "frontend/dist"), page)


@app.route("/api", methods=["POST"])
def api():
    file = flask.request.files["image"]
    file.save(f"{util.getMD5(file.filename)}.jpg")
    util.requestGemini()


app.run("0.0.0.0", port=5000)
