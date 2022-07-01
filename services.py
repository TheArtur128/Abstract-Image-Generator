from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Optional

from random import randint
from PIL import Image, ImageColor, ImageDraw
from io import BytesIO


hex_color_code = str
rgb_color_code = Iterable[int]


def convert_rgb_to_hex(color: rgb_color_code) -> hex_color_code:
    return "%02x%02x%02x" % (color[0], color[1], color[2])


def convert_hex_to_rgb(color: hex_color_code) -> rgb_color_code:
    return ImageColor.getcolor('#' + color, "RGB")


class ITokenized(ABC):
    @abstractmethod
    def generate_token(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def generate_random_token(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def create_from_token(cls, token: str):
        pass


@dataclass
class ImageElement(ITokenized):
    position: Iterable[int]
    size: Iterable[int]
    color: rgb_color_code

    def generate_token(self) -> str:
        return "{part_of_position}>{part_of_size}>{color_by_hex}".format(
            part_of_position= "p" + ":".join(map(str, self.position)),
            part_of_size="s" + ":".join(map(str, self.size)),
            color_by_hex=convert_rgb_to_hex(self.color)
        )

    @classmethod
    def generate_random_token(cls) -> str:
        return (
            f"p{randint(0, 100)}:{randint(0, 100)}>s{randint(0, 100)}:{randint(0, 100)}>"
            + convert_rgb_to_hex([randint(0, 255) for _ in range(3)])
        )

    @classmethod
    def create_from_token(cls, token: str):
        row_attributes = token.split('>')

        position, size = map(
            lambda row_attribute: tuple(map(int, row_attribute[1:].split(':'))),
            row_attributes[:2]
        )

        color = convert_hex_to_rgb(row_attributes[2])

        return cls(
            position=position,
            size=size,
            color=color
        )


class TokenizedGroup(ITokenized, ABC):
    _element_delimiter_tag: str
    _element_type: ITokenized

    def __init__(self, elements: Iterable[ITokenized]):
        self.elements = list(elements)

    def generate_token(self) -> str:
        return self._element_delimiter_tag.join(
            (element.generate_token() for element in self.elements)
        )

    @classmethod
    def generate_random_token(cls) -> str:
        return cls._element_delimiter_tag.join(
            (cls._element_type.generate_random_token() for _ in range(0, randint(4, 12)))
        )

    @classmethod
    def create_from_token(cls, token: str):
        return cls(
            map(
                lambda token_of_element: cls._element_type.create_from_token(token_of_element),
                token.split(cls._element_delimiter_tag),
            )
        )


class ImageElementGroup(TokenizedGroup):
    _element_delimiter_tag = ';'
    _element_type = ImageElement


def create_image_from_token(
    token: Optional[str] = None,
    size: Iterable[int] = (600, 600),
    backround_color: rgb_color_code = (255, 255, 255),
    groph_type: type = ImageElementGroup
) -> Image:
    if token is None:
        token = groph_type.generate_random_token()

    image = Image.new(mode="RGB", size=size, color=backround_color)

    draw = ImageDraw.Draw(image)

    for element in groph_type.create_from_token(token).elements:
        draw.rectangle(
            (
                *map(lambda procent, point: point*procent/100, element.position, size),
                *map(lambda procent, point: point*procent/100, element.size, size)
            ),
            fill=element.color
        )

    return image


def get_binary_from_image(image: Image) -> str:
    stream = BytesIO()
    image.save(stream, format="JPEG")

    return stream.getvalue()
