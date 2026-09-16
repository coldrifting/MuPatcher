from data.types.mu_file import MuFile
from data.types.mu_transform import Transform
from data.utils.errors import AttributeNotFoundError, AttributeInvalidError


def transform_remove(data: MuFile, transform_name: str):
    if len(data.root_transform.children) == 0:
        raise AttributeInvalidError("Root transform has no children and can not be removed")


    if not remove(data.root_transform.children, transform_name):
        raise AttributeNotFoundError(f"Transform with name {transform_name} not found")


def remove(transforms: list[Transform], transform_name: str) -> bool:
    for i in range(len(transforms)):
        if transforms[i].name == transform_name:
            del transforms[i]
            return True

    for child in transforms:
        if len(child.children) > 0:
            if remove(child.children, transform_name):
                return True

    return False