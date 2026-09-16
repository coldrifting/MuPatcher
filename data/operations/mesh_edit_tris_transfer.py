from data.operations.mesh_edit_tris_remove import mesh_edit_tris_remove_mesh_data
from data.operations.transform_duplicate import transform_duplicate
from data.types.mu_file import MuFile
from data.types.mu_tag import MuTag


def mesh_edit_tris_transfer(data: MuFile, obj_src_name: str, obj_dst_name: str, tris: set[int], to_new_transform: bool = False):
    source = data.get_mesh(obj_src_name)
    inverse = source.clone()

    tris_all = set(range(len(inverse.items[MuTag.MeshTriangles].triangles)))
    tris_inverse = tris_all.difference(tris)

    mesh_edit_tris_remove_mesh_data(source, tris)
    mesh_edit_tris_remove_mesh_data(inverse, tris_inverse)

    if to_new_transform:
        new_transform = transform_duplicate(data, obj_src_name, obj_dst_name, clear_mesh_data=True)
        new_transform.mesh_data = inverse
        return

    dest = data.get_mesh(obj_dst_name)
    dest.merge(inverse)