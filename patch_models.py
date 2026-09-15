import sys
import yaml
from pathlib import Path

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
from data.types.mu_file import MuFile
from data.utils.get_range import get_range
from data.utils.terminal_colors import warn

if len(sys.argv) < 2:
    warn("No patch file specified")
    warn(f"Usage: python {sys.argv[0]} /path/to/patch_file.yaml")
    exit(1)

patch_file = sys.argv[1]

with open(patch_file, "r") as file:
    patch_data = yaml.safe_load(file)

game_data_dir = Path(patch_data["game_data_dir"])
source_dir = Path(patch_data["source_dir"])
dest_dir = Path(patch_data["dest_dir"])

for file in patch_data["files"]:
    file_src = Path(game_data_dir / source_dir / file["path"])
    file_dst = Path(game_data_dir / dest_dir / file["path"])

    print(file_src.name)

    ops = file["operations"]
    if len(ops) < 1:
        continue

    mu_data = MuFile.read_file(file_src)

    for op in ops:
        match op["name"]:
            case "material_add":
                material_add(mu_data, op["material_name"], op["shader_name"])
            case "material_copy":
                material_copy(mu_data, op["material_name"], op["new_material_name"])

            case "mesh_assign_material":
                mesh_assign_material(mu_data, op["mesh_name"], op["material_name"])
            case "mesh_edit_tris_remove":
                mesh_edit_tris_remove(mu_data, op["mesh_name"], get_range(op["tris"]))
            case "mesh_edit_tris_transfer":
                mesh_edit_tris_transfer(mu_data, op["src_mesh_name"], op["dst_mesh_name"], get_range(op["tris"]))

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
                texture_edit(mu_data, op["texture_index"], op["texture_name"], op["is_normal_map"])

            case "team_colors_add":
                team_colors_edit(mu_data, op["material_name"], op["tc1_preset"], op["tc1_preset"])
            case "team_colors_edit":
                team_colors_edit(mu_data, op["material_name"], op["tc1_preset"], op["tc1_preset"])
            case _:
                raise Exception(f"Invalid mesh operation: {op['name']}")

    file_dst.parent.mkdir(parents=True, exist_ok=True)
    mu_data.write_file(file_dst)