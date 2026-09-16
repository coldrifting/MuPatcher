from data.types.mu_file import MuFile
from data.types.mu_transform import Transform


def transform_duplicate(data: MuFile, transform_name: str, new_transform_name: str, clear_mesh_data: bool = False) -> Transform:
    return data.clone_transform(transform_name, new_transform_name, clear_mesh_data)