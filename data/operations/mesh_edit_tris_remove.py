from data.types.mu_file import MuFile
from data.types.mu_tag import MuTag
from data.types.transform.mesh.mesh_data import MeshData
from data.types.transform.mesh.mesh_data_item import MeshDataItemTriangles


def mesh_edit_tris_remove(data: MuFile, mesh_name: str, tris: list[int]) -> MeshData:
    source = data.get_mesh(mesh_name)

    vertex_uses_old: dict[int, int] = {}
    for i in range(source.vertex_count):
        vertex_uses_old[i] = 0

    triangles = source.items[MuTag.MeshTriangles]
    match triangles:
        case MeshDataItemTriangles():
            for i in range(len(triangles.triangles)):
                vertex_uses_old[triangles.triangles[i].x] += 1
                vertex_uses_old[triangles.triangles[i].y] += 1
                vertex_uses_old[triangles.triangles[i].z] += 1

            for i in reversed(range(len(triangles.triangles))):
                if i in tris:
                    vertex_uses_old[triangles.triangles[i].x] -= 1
                    vertex_uses_old[triangles.triangles[i].y] -= 1
                    vertex_uses_old[triangles.triangles[i].z] -= 1


    # Generate removal data
    vertices_to_remove = [x for x in vertex_uses_old if vertex_uses_old[x] == 0]

    new_vertex_mapping: dict[int, int] = {}

    new_index_remain = 0
    new_index_extract = 0
    for old_index in range(source.vertex_count):
        if old_index in vertices_to_remove:
            new_vertex_mapping[old_index] = new_index_extract
            new_index_extract += 1
        else:
            new_vertex_mapping[old_index] = new_index_remain
            new_index_remain += 1

    clipboard: MeshData = MeshData(len(vertices_to_remove), 1)

    # Pull out removed data for insertion into another mesh if desired
    clipboard.items[MuTag.MeshVertices] = source.items[MuTag.MeshVertices].cut(vertices_to_remove)

    for tag in [MuTag.MeshUv, MuTag.MeshUv2, MuTag.MeshNormals, MuTag.MeshTangents, MuTag.MeshBoneWeights, MuTag.MeshVertexColors]:
        if source.items.get(tag) is not None:
            clipboard.items[tag] = source.items[tag].cut(vertices_to_remove)

    clipboard.items[MuTag.MeshTriangles] = source.items[MuTag.MeshTriangles].cut(vertices_to_remove, new_vertex_mapping)

    source.vertex_count -= len(vertices_to_remove)

    return clipboard