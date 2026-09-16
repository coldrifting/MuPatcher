from data.types.core.vec3 import Vec3
from data.types.mu_file import MuFile
from data.types.mu_tag import MuTag
from data.types.transform.mesh.mesh_data_item import MeshDataItemNormals
from data.utils.errors import AttributeNotFoundError


def mesh_average_normals(mu_data: MuFile, transform_name: str, vertex_groups: list[list[int]]):
    mesh = mu_data.get_mesh(transform_name)

    normals_data: MeshDataItemNormals = mesh.items.get(MuTag.MeshNormals, None)
    if normals_data is None:
        raise AttributeNotFoundError(f"No normals defined for mesh {transform_name}")

    if not isinstance(normals_data, MeshDataItemNormals):
        return

    normals: list[Vec3] = normals_data.normals
    for i in range(len(vertex_groups)):
        sum_vec = Vec3(0,0,0)
        for j in range(len(vertex_groups[i])):
            sum_vec += normals[vertex_groups[i][j]]

        normalized = sum_vec.normalize()

        for j in range(len(vertex_groups[i])):
            normals[vertex_groups[i][j]] = normalized
