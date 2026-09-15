from data.types.mu_file import MuFile
from data.types.mu_transform import Transform


def mesh_assign_material(data: MuFile, mesh_name: str, material_name: str):
    mat_index = data.get_material_index(material_name)
    edit(data.root_transform, mesh_name, mat_index)

def edit(transform: Transform, target: str, mat_index: int):
    if transform.name == target:
        if transform.mesh_data is not None:
            if transform.mesh_data.render_settings is not None:
                transform.mesh_data.render_settings.material_index = mat_index

        if transform.skinned_mesh_data is not None:
            if transform.skinned_mesh_data.mesh_data is not None:
                if transform.skinned_mesh_data.mesh_data.render_settings is not None:
                    transform.skinned_mesh_data.mesh_data.render_settings.material_index = mat_index

        return

    for child in transform.children:
        edit(child, target, mat_index)