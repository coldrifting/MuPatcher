## MuPatcher

A configurable patcher for scripting changes to KSP Mu model files, written in Python, with a focus on adjusting materials and adding ReStockPBR/Technicolor support.

Designed to allow patch creators to share changes and fixes to otherwise All Rights Reserved model files, without breaking the license. No actual art assets are shared, just a small yaml confing file. 

An example config file is shared below:

#### patch.yaml
```yaml patch.yaml
game_data_dir: "C:/Steam/steamapps/common/Kerbal Space Program/GameData"
dest_dir: "ReStockPBR_Patch"
files:
  - path: "RestockPBR/Assets/Command/restock-pbr-cockpit-mk2-1.mu"
    operations:
      - name: "mesh_edit_tris_transfer"
        src_mesh_name: "Mk2CockpitPointyTiles"
        dst_mesh_name: "Mk2CockpitPointyTilesLower"
        tris: 303-376
      - name: "material_copy"
        material_name: "restock-pbr-cockpit-mk2-1"
        new_material_name: "restock-pbr-cockpit-mk2-1-tiles"
      - name: "team_colors_edit"
        material_name: "restock-pbr-cockpit-mk2-1-tiles"
        tc1_preset: "tileBlack"
        tc2_preset: "blank"
      - name: "mesh_assign_material"
        transform_name: "Mk2CockpitPointyTilesLower"
        material_name: "restock-pbr-cockpit-mk2-1-tiles"
```

To try it out, save the above patch.yaml file somewhere, make sure you have the correct game data path in the file, and that you have ReStockPBR installed.
Then run the following command, changing `/path/to/patch.yaml` to where you saved the file:

`
python mu_patcher.py /path/to/patch.yaml
`

This config file moves some faces from one transform to another in order to get all the areas with added tiles from ReStockPBR onto one transform/mesh.
Once this is done, the material assigned to the tiles mesh is duplicated and edited, allowing for correct looking part thumbnail visuals. 

This example also shows off some of the included convenience functions for setting mesh default materials to use ReStockPBR/Technicolor's default swatches.
There is also a function `team_colors_add`, which will let you easily add the Technicolor `Resurfaced/Standard (TC)` shader and its prerequisite textures, floats, and colors to the material settings.