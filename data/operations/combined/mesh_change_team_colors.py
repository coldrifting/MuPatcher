from data.operations.combined.team_colors_edit import team_colors_edit
from data.operations.material_copy import material_copy
from data.operations.mesh_assign_material import mesh_assign_material
from data.types.mu_file import MuFile
from data.utils.errors import AttributeNotFoundError


def mesh_change_team_colors(mu_data: MuFile, transform_name: str, material_suffix: str, tc1_name: str, tc2_name: str | None = None):
    mesh_data = mu_data.get_mesh(transform_name)
    index = mesh_data.render_settings.material_index
    if index is None:
        raise AttributeNotFoundError("No material applied to target transform")

    if index not in range(len(mu_data.materials)):
        raise AttributeNotFoundError(f"Material index {index} out of range. Valid ranges: 0 - {len(mu_data.materials)-1}")

    material = mu_data.materials[index]

    material_copy(mu_data, material.name, material.name + "-" + material_suffix)
    team_colors_edit(mu_data, material.name + "-" + material_suffix, tc1_name, tc2_name)
    mesh_assign_material(mu_data, transform_name, material.name + "-" + material_suffix)