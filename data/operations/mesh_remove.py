from data.types.mu_file import MuFile
from data.types.mu_transform import Transform


def mesh_remove(data: MuFile, name: str):
    remove(data.root_transform, name)


def remove(transform: Transform, target: str):
    if transform.name == target:
        transform.mesh_data = None
        return

    for child in transform.children:
        remove(child, target)