from data.types.material.texture import Texture
from data.types.mu_file import MuFile


def texture_edit(data: MuFile, texture_name_old: int, texture_name_new: str, is_normal_map: bool):
    texture_index = data.get_texture_index(texture_name_old)
    data.textures[texture_index] = Texture(texture_name_new, is_normal_map)