import json
from os import path
from . import util

apikey: dict = json.load(open(path.join(util.cwd, "backend/config/apikey.json")))
