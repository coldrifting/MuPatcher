import sys
from typing import Tuple

import yaml
from pathlib import Path

from data.operations.combined.mesh_change_team_colors import mesh_change_team_colors
from data.operations.combined.team_colors_add import team_colors_add
from data.operations.combined.team_colors_edit import team_colors_edit
from data.operations.material_add import material_add
from data.operations.material_copy import material_copy
from data.operations.mesh_assign_material import mesh_assign_material
from data.operations.mesh_average_normals import mesh_average_normals
from data.operations.mesh_edit_set_uvs import mesh_edit_set_uvs
from data.operations.mesh_edit_set_vertices import mesh_edit_set_vertices
from data.operations.mesh_edit_tris_remove import mesh_edit_tris_remove
from data.operations.mesh_edit_tris_transfer import mesh_edit_tris_transfer
from data.operations.mesh_remove import mesh_remove
from data.operations.property_add import property_add
from data.operations.property_edit import property_edit
from data.operations.shader_edit import shader_edit
from data.operations.texture_add import texture_add
from data.operations.texture_edit import texture_edit
from data.operations.transform_duplicate import transform_duplicate
from data.operations.transform_merge import transform_merge
from data.operations.transform_remove import transform_remove
from data.types.mu_file import MuFile
from data.utils.errors import AttributeInvalidError, AttributeNotFoundError, AttributeAlreadyExistsError
from data.utils.get_or_error import get_or_error
from data.utils.get_groups import get_groups
from data.utils.get_range import get_range
from data.utils.get_uv_data import get_uv_data
from data.utils.get_vertex_data import get_vertex_data
from data.utils.terminal_colors import warn, error

print("[Patching Meshes]")

try:
    if len(sys.argv) < 2:
        warn("No patch file specified")
        warn(f"Usage: python {sys.argv[0]} /path/to/patch_file.yaml")
        exit(1)

    patch_file = sys.argv[1]

    if not Path(patch_file).exists():
        error(f"Patch file {patch_file} not found")
        exit(1)

    with open(patch_file, "r") as file:
        patch_data = yaml.safe_load(file)

    game_data_str = get_or_error(patch_data, "game_data_dir")
    dest_dir_str = get_or_error(patch_data, "dest_dir")

    game_data_dir = Path(game_data_str)
    dest_dir = Path(game_data_dir / dest_dir_str)

    files_in: list[Path] = []
    output: list[Tuple[Path, bytes]] = []

    files_list: list[str] = get_or_error(patch_data, "files")
    for file in files_list:
        model_name = get_or_error(file, "path")
        if not model_name.endswith(".mu"):
            model_name += ".mu"

        file_src = Path(game_data_dir / model_name)
        if not file_src.exists():
            raise FileNotFoundError(f"File {file_src} not found")

        files_in.append(file_src)

    for index, file in enumerate(files_list):
        model_name = get_or_error(file, "path")
        if not model_name.endswith(".mu"):
            model_name += ".mu"

        file_src = files_in[index]

        # Replace root folder of asset in game data dir with dest dir
        file_dst = Path(dest_dir / Path(*Path(model_name).parts[1:]))

        print(model_name)

        ops = get_or_error(file, "operations")
        if len(ops) < 1:
            warn(f"WARNING: {model_name} has no operations defined")
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
                case "mesh_average_normals":
                    mesh_average_normals(mu_data, op["transform_name"], get_groups(op["vertex_groups"]))
                case "mesh_change_team_colors":
                    mesh_change_team_colors(mu_data, op["transform_name"], op["material_suffix"], op["tc1_preset"], op["tc2_preset"])
                case "mesh_edit_set_uvs":
                    mesh_edit_set_uvs(mu_data, op["transform_name"], get_uv_data(op["uvs"]))
                case "mesh_edit_set_vertices":
                    mesh_edit_set_vertices(mu_data, op["transform_name"], get_vertex_data(op["vertices"]))
                case "mesh_edit_tris_remove":
                    mesh_edit_tris_remove(mu_data, op["transform_name"], get_range(op["tris"]))
                case "mesh_edit_tris_transfer":
                    to_new_transform: bool = op.get("create_transform", False)
                    mesh_edit_tris_transfer(mu_data, op["transform_name_src"], op["transform_name_dst"], get_range(op["tris"]), to_new_transform)

                case "mesh_remove":
                    mesh_remove(mu_data, op["mesh_name"])

                case "property_add":
                    property_add(mu_data, op["material_name"], op["property_name"], op["property_type"], op["value"])
                case "property_edit":
                    property_edit(mu_data, op["material_name"], op["property_name"], op["value"])

                case "shader_edit":
                    shader_edit(mu_data, op["material_name"], op["shader_name"])

                case "texture_add":
                    texture_add(mu_data, op["texture_name"], op.get("is_normal_map", False))
                case "texture_edit":
                    texture_edit(mu_data, op["texture_name"], op["new_texture_name"], op.get("is_normal_map", False))

                case "team_colors_add":
                    team_colors_add(mu_data, op["material_name"], op["tc1_preset"], op["tc2_preset"])
                case "team_colors_edit":
                    team_colors_edit(mu_data, op["material_name"], op["tc1_preset"], op["tc2_preset"])

                case "transform_duplicate":
                    transform_duplicate(mu_data, op["transform_name"], op["new_transform_name"])
                case "transform_merge":
                    transform_merge(mu_data, op["transform_name_primary"], op["transform_name_secondary"])
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