from data.types.mu_file import MuFile
from data.utils.errors import AttributeInvalidError, AttributeNotFoundError


def transform_merge(data: MuFile, transform_name_primary: str, transform_name_secondary: str):
    if len(data.root_transform.children) == 0:
        raise AttributeInvalidError("Root transform has no children and can not be merged")

    data.merge_transforms(transform_name_primary, transform_name_secondary)
