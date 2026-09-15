from data.types.mu_file import MuFile


def shader_edit(data: MuFile, material_name: str, shader: str):
    material = data.get_material(material_name)
    material.shader_name = shader
