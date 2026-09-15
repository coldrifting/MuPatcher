from data.operations.mesh_edit_tris_remove import mesh_edit_tris_remove
from data.types.mu_file import MuFile
from data.types.mu_tag import MuTag


def mesh_edit_tris_transfer(data: MuFile, obj_src: str, obj_dst: str, tris: list[int]):
    clipboard = mesh_edit_tris_remove(data, obj_src, tris)
    dest = data.get_mesh(obj_dst)

    dest.items[MuTag.MeshVertices].paste(clipboard.items[MuTag.MeshVertices])

    for tag in [MuTag.MeshUv, MuTag.MeshUv2, MuTag.MeshNormals, MuTag.MeshTangents, MuTag.MeshBoneWeights, MuTag.MeshVertexColors]:
        if clipboard.items.get(tag) is not None and dest.items.get(tag) is not None:
            dest.items[tag].paste(clipboard.items[tag])

    dest.items[MuTag.MeshTriangles].paste(clipboard.items[MuTag.MeshTriangles], dest.vertex_count)
    dest.vertex_count += len(clipboard.items[MuTag.MeshVertices].vertices)
