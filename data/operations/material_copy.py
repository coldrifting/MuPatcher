from data.types.mu_file import MuFile


def material_copy(data: MuFile, material_name: str, new_material_name: str):
    material = data.get_material(material_name)
    material_new = material.clone(new_name=new_material_name)
    data.materials.append(material_new)