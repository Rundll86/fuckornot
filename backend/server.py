import flask, base64, sys, argparse
from os import path
from flask_cors import CORS
from engine import util

NO_GIVEN = "no given anything"
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--apikey", type=str, default=NO_GIVEN, required=True)
args = parser.parse_args()
apikey = args.apikey
app = flask.Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def index():
    return flask.redirect("/index.html")


@app.route("/<path:page>")
def showPage(page):
    return flask.send_from_directory(path.join(util.cwd, "frontend/dist"), page)


@app.route("/api", methods=["POST"])
def api():
    if "image" not in flask.request.files and "image" in flask.request.form:
        imageData = flask.request.form["image"]
        if imageData.startswith("data:image"):
            imageData = imageData.split(",")[1]
        imageBytes = base64.b64decode(imageData)
        savePath = path.join(
            util.cwd, "data", f"{util.getMD5(str(hash(imageBytes)))}.jpg"
        )
        with open(savePath, "wb") as f:
            f.write(imageBytes)
    else:
        file = flask.request.files["image"]
        savePath = path.join(util.cwd, "data", f"{util.getMD5(str(file.filename))}.jpg")
        file.save(savePath)
        imageBytes = open(savePath, "rb").read()
    soul = flask.request.form.get("soul", "desire_avatar")
    response = util.requestGemini(
        f"https://api-proxy.me/gemini/v1beta/models/gemini-2.5-flash-lite-preview-06-17:generateContent?key={apikey}",
        soul,
        imageBytes,
        flask.request.form.get("language", "中文"),
    )
    print(response)
    return response["candidates"][0]["content"]["parts"][0]["text"]


app.run("0.0.0.0", port=5000)
