from typing import Optional

from flask import request, Response
from flask_restful import Resource
from io import BytesIO

from services import create_image_from_token, convert_hex_to_rgb, ImageElementGroup


class RandomImage(Resource):
    def get(self, token: Optional[str] = None):
        stream = BytesIO()

        parsed_arguments = dict(request.args)

        if "size" in parsed_arguments.keys():
            parsed_arguments["size"] = (int(parsed_arguments["size"]),) * 2

        if "backround_color" in parsed_arguments.keys():
            parsed_arguments["backround_color"] = convert_hex_to_rgb(parsed_arguments["backround_color"])

        create_image_from_token(
            token=token,
            **parsed_arguments
        ).save(stream, format="JPEG")

        return Response(stream.getvalue(), content_type="image/jpeg")


class RandomImageToken(Resource):
    def get(self):
        return Response(ImageElementGroup.generate_random_token(), content_type="text")
