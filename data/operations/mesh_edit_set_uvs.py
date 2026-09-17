from data.types.core.vec2 import Vec2
from data.types.mu_file import MuFile
from data.types.mu_tag import MuTag
from data.types.transform.mesh.mesh_data_item import MeshDataItemUvs


def mesh_edit_set_uvs(mu_data: MuFile, transform_name: str, uvs: dict[int,Vec2]):
    mesh = mu_data.get_mesh(transform_name)

    uv_data = mesh.items[MuTag.MeshUv]
    if not isinstance(uv_data, MeshDataItemUvs):
        return

    for uv_index in uvs.keys():
        uv_data.uvs[uv_index] = uvs[uv_index]