from flask_restful import Api
from flask import Flask

from resources import RandomImage, RandomImageToken, RandomFavicon


app = Flask(__name__)
api = Api(app)

api.add_resource(RandomImage, '/', "/<string:token>", "/random-image", "/random-image/<string:token>")
api.add_resource(RandomImageToken, "/random-image-token")
api.add_resource(RandomFavicon, "/favicon.ico")
