from typing import Optional

from flask import request, Response
from flask_restful import Resource

from services import create_image_from_token, convert_hex_to_rgb, ImageElementGroup, get_binary_from_image


class RandomImage(Resource):
    def get(self, token: Optional[str] = None):
        parsed_arguments = dict(request.args)

        if 'size' in parsed_arguments.keys():
            parsed_arguments['size'] = (int(parsed_arguments['size']),) * 2

        if "backround_color" in parsed_arguments.keys():
            parsed_arguments["backround_color"] = convert_hex_to_rgb(parsed_arguments["backround_color"])

        return Response(
            get_binary_from_image(create_image_from_token(token=token, **parsed_arguments)),
            content_type="image/jpeg"
        )


class RandomImageToken(Resource):
    def get(self):
        return Response(ImageElementGroup.generate_random_token(), content_type='text')


class RandomFavicon(Resource):
    def get(self):
        return Response(
            get_binary_from_image(create_image_from_token(size=(16, 16), backround_color=(90,)*3)),
            content_type="image/jpeg"
        )
