from data.types.material.texture import Texture
from data.types.mu_file import MuFile


def texture_edit(data: MuFile, texture_index: int, texture_name: str, is_normal_map: bool):
    if texture_index >= len(data.materials):
        raise Exception(f'Texture index {texture_index} out of range')

    data.textures[texture_index] = Texture(texture_name, is_normal_map)