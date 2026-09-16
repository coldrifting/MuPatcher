import sys
from typing import Tuple

import yaml
from pathlib import Path

from data.operations.combined.team_colors_add import team_colors_add
from data.operations.combined.team_colors_edit import team_colors_edit
from data.operations.material_add import material_add
from data.operations.material_copy import material_copy
from data.operations.mesh_assign_material import mesh_assign_material
from data.operations.mesh_edit_tris_remove import mesh_edit_tris_remove
from data.operations.mesh_edit_tris_transfer import mesh_edit_tris_transfer
from data.operations.mesh_remove import mesh_remove
from data.operations.property_add import property_add
from data.operations.property_edit import property_edit
from data.operations.shader_edit import shader_edit
from data.operations.texture_add import texture_add
from data.operations.texture_edit import texture_edit
from data.operations.transform_remove import transform_remove
from data.types.mu_file import MuFile
from data.utils.errors import AttributeInvalidError, AttributeNotFoundError, AttributeAlreadyExistsError
from data.utils.get_range import get_range
from data.utils.terminal_colors import warn, error

if len(sys.argv) < 2:
    warn("No patch file specified")
    warn(f"Usage: python {sys.argv[0]} /path/to/patch_file.yaml")
    exit(1)

patch_file = sys.argv[1]

with open(patch_file, "r") as file:
    patch_data = yaml.safe_load(file)

game_data_dir = Path(patch_data["game_data_dir"])
dest_dir = Path(patch_data["dest_dir"])

output: list[Tuple[Path, bytes]] = []

try:
    for file in patch_data["files"]:

        model_name = file["path"]
        if not model_name.endswith(".mu"):
            model_name += ".mu"

        file_src = Path(game_data_dir / model_name)

        # Replace root folder of asset in game data dir with dest dir
        file_dst = Path(game_data_dir / dest_dir / Path(*Path(model_name).parts[1:]))

        print(model_name)

        ops = file["operations"]
        if len(ops) < 1:
            continue

        if not file_src.exists():
            raise FileNotFoundError(f"File {file_src} does not exist. Skipping...")

        mu_data = MuFile.read_file(file_src)

        for op in ops:
            match op["name"]:
                case "material_add":
                    material_add(mu_data, op["material_name"], op["shader_name"])
                case "material_copy":
                    material_copy(mu_data, op["material_name"], op["new_material_name"])

                case "mesh_assign_material":
                    mesh_assign_material(mu_data, op["transform_name"], op["material_name"])
                case "mesh_edit_tris_remove":
                    mesh_edit_tris_remove(mu_data, op["transform_name"], get_range(op["tris"]))
                case "mesh_edit_tris_transfer":
                    mesh_edit_tris_transfer(mu_data, op["transform_name_src"], op["transform_name_dst"], get_range(op["tris"]))

                case "mesh_remove":
                    mesh_remove(mu_data, op["mesh_name"])

                case "property_add":
                    property_add(mu_data, op["material_name"], op["property_name"], op["property_type"], op["value"])
                case "property_edit":
                    property_edit(mu_data, op["material_name"], op["property_name"], op["value"])

                case "shader_edit":
                    shader_edit(mu_data, op["material_name"], op["shader_name"])

                case "texture_add":
                    texture_add(mu_data, op["texture_name"], op["is_normal_map"])
                case "texture_edit":
                    texture_edit(mu_data, op["texture_name"], op["new_texture_name"], op.get("is_normal_map", False))

                case "team_colors_add":
                    team_colors_add(mu_data, op["material_name"], op["tc1_preset"], op["tc1_preset"])
                case "team_colors_edit":
                    team_colors_edit(mu_data, op["material_name"], op["tc1_preset"], op["tc1_preset"])

                case "transform_remove":
                    transform_remove(mu_data, op["transform_name"])

                case _:
                    raise AttributeInvalidError(f"Invalid mesh operation: {op['name']}")

        data_output = mu_data.write()
        output.append((file_dst, data_output))

    for file_path, data in output:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(data)

except (FileNotFoundError, AttributeNotFoundError, AttributeInvalidError, AttributeAlreadyExistsError) as e:
    if sys.gettrace() is not None:
        raise

    error(str(e))
    exit(1)