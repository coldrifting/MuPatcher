from data.types.core.vec3 import Vec3
from data.types.mu_file import MuFile
from data.types.mu_tag import MuTag
from data.types.transform.mesh.mesh_data_item import MeshDataItemVertices


def mesh_edit_set_vertices(mu_data: MuFile, transform_name: str, vertices: dict[int,Vec3]):
    mesh = mu_data.get_mesh(transform_name)

    vertices_data = mesh.items[MuTag.MeshVertices]
    if not isinstance(vertices_data, MeshDataItemVertices):
        return

    for vertex_index in vertices.keys():
        vertices_data.vertices[vertex_index] = vertices[vertex_index]
