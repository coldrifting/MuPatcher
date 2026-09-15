from data.types.material.texture import Texture
from data.types.mu_file import MuFile


def texture_add(data: MuFile, name: str, is_normal_map: bool):
    texture = Texture(name, is_normal_map)
    data.textures.append(texture)