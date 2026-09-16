from data.types.material.material_property import MaterialPropertyColor, MaterialPropertyFloat2, MaterialPropertyVector, \
    MaterialPropertyFloat3, MaterialPropertyTexture
from data.types.mu_file import MuFile


def property_edit(data: MuFile, material_name: str, property_name: str, value):
    prop = data.get_property(material_name, property_name)

    match prop:
        case MaterialPropertyColor():
            prop.color = value
        case MaterialPropertyVector():
            prop.value = value
        case MaterialPropertyFloat2():
            prop.value = value
        case MaterialPropertyFloat3():
            prop.value = value
        case MaterialPropertyTexture():
            prop.texture_index = data.get_texture_index(value)