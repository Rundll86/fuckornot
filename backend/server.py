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
    savePath = path.join(util.cwd, "data", f"{util.getMD5(str(file.filename))}.jpg")
    file.save(savePath)

    imageData = open(savePath, "rb").read()
    apikey = flask.request.form.get("key", "")
    soul = flask.request.form.get("soul", "desire_avatar")
    return util.requestGemini(
        f"https://api-proxy.me/gemini/v1beta/models/gemini-2.5-flash-lite-preview-06-17:generateContent?key={apikey}",
        soul,
        imageData,
        flask.request.form.get("language", "中文"),
    )["candidates"][0]["content"]["parts"][0]["text"]


app.run("0.0.0.0", port=5000)
