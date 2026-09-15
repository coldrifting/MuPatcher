from data.types.core.vec2 import Vec2
from data.types.material.material_property import MaterialPropertyColor, MaterialProperty, MaterialPropertyFloat3, \
    MaterialPropertyTexture
from data.types.mu_file import MuFile


def property_add(data: MuFile, material_name: str, property_name: str, property_type: str, value):
    prop = data.get_property(material_name, property_name)
    if prop is not None:
        raise Exception(f'Property {property_name} already exists in material')

    material = data.get_material(material_name)

    match property_type:
        case "Color":
            prop: MaterialProperty = MaterialPropertyColor(property_name, value)
        case "Float":
            prop: MaterialProperty = MaterialPropertyFloat3(property_name, value)
        case "Texture":
            prop: MaterialProperty = MaterialPropertyTexture(property_name, value, Vec2(1,1), Vec2(0,0))
        case _:
            raise Exception(f'Property type {property_type} invalid')

    material.properties.append(prop)