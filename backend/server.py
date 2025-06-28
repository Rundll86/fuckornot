import flask
from os import path
from engine import util, config


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
    savePath = path.join(util.cwd, "data", f"{util.getMD5(file.filename)}.jpg")
    file.save(savePath)

    imageData = open(savePath, "rb").read()
    apikey = config.apikey["gemini"]
    soul = flask.request.form.get("soul", "desire_avatar")
    util.requestGemini(
        f"https://api-proxy.me/gemini/v1beta/models/gemini-2.5-flash-lite-preview-06-17:generateContent?key={apikey}",
        soul,
        imageData,
    )
    return ""


app.run("0.0.0.0", port=5000)
