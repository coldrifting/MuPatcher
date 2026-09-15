from data.operations.property_edit import property_edit
from data.types.mu_file import MuFile
from data.utils.team_color import TeamColorDb


def team_colors_edit(data: MuFile, name: str, tc1_name: str, tc2_name: str | None = None):
    if tc2_name is None:
        tc2_name = tc1_name

    tc1 = TeamColorDb[tc1_name]
    tc2 = TeamColorDb[tc2_name]

    property_edit(data, name, "_TC1Color", tc1.color)
    property_edit(data, name, "_TC1Metalness", tc1.metalness)
    property_edit(data, name, "_TC1Smoothness", tc1.smoothness)
    property_edit(data, name, "_TC1MetalBlend", tc1.metal_blend)
    property_edit(data, name, "_TC1SmoothBlend", tc1.smooth_blend)

    property_edit(data, name, "_TC2Color", tc2.color)
    property_edit(data, name, "_TC2Metalness", tc2.metalness)
    property_edit(data, name, "_TC2Smoothness", tc2.smoothness)
    property_edit(data, name, "_TC2MetalBlend", tc2.metal_blend)
    property_edit(data, name, "_TC2SmoothBlend", tc2.smooth_blend)