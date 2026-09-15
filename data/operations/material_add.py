from data.types.material.material import Material
from data.types.mu_file import MuFile
from data.types.mu_transform import Transform


def material_add(data: MuFile, name: str, shader: str):
    material = Material(name, shader, [])
    data.materials.append(material)
    edit(data.root_transform, len(data.materials))

def edit(transform: Transform, mat_count: int):
    if transform.mesh_data is not None:
        if transform.mesh_data.render_settings is not None:
            transform.mesh_data.render_settings.material_count = mat_count

    if transform.skinned_mesh_data is not None:
        if transform.skinned_mesh_data.mesh_data is not None:
            if transform.skinned_mesh_data.mesh_data.render_settings is not None:
                transform.skinned_mesh_data.mesh_data.render_settings.material_count = mat_count

    for child in transform.children:
        edit(child, mat_count)