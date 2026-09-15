from data.operations.property_add import property_add
from data.operations.texture_add import texture_add
from data.types.material.material import Material
from data.types.material.material_property import MaterialPropertyTexture
from data.types.mu_file import MuFile
from data.utils.team_color import TeamColorDb


def team_colors_add(data: MuFile, name: str, tc1_name: str, tc2_name: str | None = None):
    mat: Material = data.materials[name]
    if mat is None:
        raise Exception(f'Material with name {name} not found in file')

    if tc2_name is None:
        tc2_name = tc1_name

    tc1 = TeamColorDb[tc1_name]
    tc2 = TeamColorDb[tc2_name]

    property_add(data, name, "_TC1Color", "Color", tc1.color)
    property_add(data, name, "_TC1Metalness", "Float", tc1.metalness)
    property_add(data, name, "_TC1Smoothness", "Float", tc1.smoothness)
    property_add(data, name, "_TC1MetalBlend", "Float", tc1.metal_blend)
    property_add(data, name, "_TC1SmoothBlend", "Float", tc1.smooth_blend)

    property_add(data, name, "_TC2Color", "Color", tc2.color)
    property_add(data, name, "_TC2Metalness", "Float", tc2.metalness)
    property_add(data, name, "_TC2Smoothness", "Float", tc2.smoothness)
    property_add(data, name, "_TC2MetalBlend", "Float", tc2.metal_blend)
    property_add(data, name, "_TC2SmoothBlend", "Float", tc2.smooth_blend)

    property_add(data, name, "_MetalMap", "Texture", len(data.textures) + 1)
    property_add(data, name, "_TeamColorMap", "Texture", len(data.textures) + 2)

    index = -1
    for prop in mat.properties:
        if prop.name == "_MainTex":
            match prop:
                case MaterialPropertyTexture():
                    index = prop.texture_index

    if index == -1:
        raise Exception(f'Main Texture name for material {name} not found')

    main_texture_name = data.textures[index].name

    split = main_texture_name.rsplit('.', 1)
    name = split[0]
    ext = split[1]

    texture_add(data, name + "-m" + ext, False)
    texture_add(data, name + "-tc" + ext, False)
