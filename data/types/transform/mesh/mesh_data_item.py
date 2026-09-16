from data.types.core.byte_reader import ByteReader
from data.types.core.byte_writer import ByteWriter
from data.types.core.color_byte import ColorByte
from data.types.core.vec2 import Vec2
from data.types.core.vec3 import Vec3
from data.types.core.vec4 import Vec4
from data.types.core.int3 import Int3
from data.types.core.int4 import Int4
from data.types.mu_tag import MuTag


class MeshDataItem:
    def write(self, writer: ByteWriter):
        pass

    @staticmethod
    def read(reader: ByteReader, vertex_count: int) -> 'MeshDataItem':
        match reader.preview():
            case MuTag.MeshVertices:
                return MeshDataItemVertices.read_sub(reader, vertex_count)
            case MuTag.MeshUv:
                return MeshDataItemUvs.read_sub(reader, vertex_count)
            case MuTag.MeshUv2:
                return MeshDataItemUvs.read_sub(reader, vertex_count)
            case MuTag.MeshNormals:
                return MeshDataItemNormals.read_sub(reader, vertex_count)
            case MuTag.MeshTangents:
                return MeshDataItemTangents.read_sub(reader, vertex_count)
            case MuTag.MeshTriangles:
                return MeshDataItemTriangles.read_sub(reader)
            case MuTag.MeshBoneWeights:
                return MeshDataItemBoneWeights.read_sub(reader, vertex_count)
            case MuTag.MeshBindPoses:
                return MeshDataItemBindPoses.read_sub(reader)
            case MuTag.MeshVertexColors:
                return MeshDataItemVertexColors.read_sub(reader, vertex_count)

        raise Exception(f"Unknown tag with id: {reader.preview()}")


class MeshDataItemBindPoses(MeshDataItem):
    def __init__(self, poses: list[int]):
        self.poses = poses

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshBindPoses)
        writer.write_int(len(self.poses) // 16)
        for pose in self.poses:
            writer.write_int(pose)

    @staticmethod
    def read_sub(reader: ByteReader) -> 'MeshDataItemBindPoses':
        reader.read_int()  # Consume Tag
        num_poses = reader.read_int() * 16

        poses = []
        for _ in range(num_poses):
            poses.append(reader.read_int())

        return MeshDataItemBindPoses(
            poses = poses
        )


class BoneWeight:
    def __init__(self, indices: Int4, weights: Vec4):
        self.indices = indices
        self.weights = weights


class MeshDataItemBoneWeights(MeshDataItem):
    def __init__(self, bone_weights: list[BoneWeight]):
        self.bone_weights = bone_weights

    def cut(self, cut_indices: list[int]) -> 'MeshDataItemBoneWeights':
        cut_bone_weights = []
        for i in reversed(range(len(self.bone_weights))):
            if i in cut_indices:
                cut_bone_weights.append(self.bone_weights[i])
                del self.bone_weights[i]

        return MeshDataItemBoneWeights(list(reversed(cut_bone_weights)))

    def paste(self, pasted_bone_weights: 'MeshDataItemBoneWeights'):
        for bone_weight in pasted_bone_weights.bone_weights:
            self.bone_weights.append(bone_weight)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshBoneWeights)
        for bone_weight in self.bone_weights:
            writer.write_int4(bone_weight.indices)
            writer.write_vec4(bone_weight.weights)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemBoneWeights':
        reader.read_int()  # Consume Tag

        bone_weights = []
        for _ in range(vertex_count):
            bone_weight_indices = reader.read_int4()
            bone_weight_weights = reader.read_vec4()
            bone_weights.append(BoneWeight(bone_weight_indices, bone_weight_weights))

        return MeshDataItemBoneWeights(
            bone_weights = bone_weights
        )

class MeshDataItemNormals(MeshDataItem):
    def __init__(self, normals: list[Vec3]):
        self.normals = normals

    def cut(self, cut_indices: list[int]) -> 'MeshDataItemNormals':
        cut_normals = []
        for i in reversed(range(len(self.normals))):
            if i in cut_indices:
                cut_normals.append(self.normals[i])
                del self.normals[i]

        return MeshDataItemNormals(list(reversed(cut_normals)))

    def paste(self, pasted_normals: 'MeshDataItemNormals'):
        for normal in pasted_normals.normals:
            self.normals.append(normal)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshNormals)
        for vertex in self.normals:
            writer.write_vec3(vertex)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemNormals':
        reader.read_int()  # Consume Tag

        normals = []
        for _ in range(vertex_count):
            normals.append(reader.read_vec3())

        return MeshDataItemNormals(
            normals = normals
        )


class MeshDataItemTangents(MeshDataItem):
    def __init__(self, tangents: list[Vec4]):
        self.tangents = tangents

    def cut(self, cut_indices: list[int]) -> 'MeshDataItemTangents':
        cut_tangents = []
        for i in reversed(range(len(self.tangents))):
            if i in cut_indices:
                cut_tangents.append(self.tangents[i])
                del self.tangents[i]

        return MeshDataItemTangents(list(reversed(cut_tangents)))

    def paste(self, pasted_tangents: 'MeshDataItemTangents'):
        for tangent in pasted_tangents.tangents:
            self.tangents.append(tangent)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshTangents)
        for normal in self.tangents:
            writer.write_vec4(normal)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemTangents':
        reader.read_int()  # Consume Tag

        tangents = []
        for _ in range(vertex_count):
            tangents.append(reader.read_vec4())

        return MeshDataItemTangents(
            tangents = tangents
        )


class MeshDataItemTriangles(MeshDataItem):
    def __init__(self, triangles: list[Int3]):
        self.triangles = triangles

    def cut(self, cut_indices: list[int], new_mapping: dict[int,int]) -> 'MeshDataItemTriangles':
        cut_triangles = []
        for i in reversed(range(len(self.triangles))):
            if (self.triangles[i].x in cut_indices) or (self.triangles[i].y in cut_indices) or (self.triangles[i].z in cut_indices):
                cut_triangles.append(
                    Int3(
                        new_mapping[self.triangles[i].x],
                        new_mapping[self.triangles[i].y],
                        new_mapping[self.triangles[i].z]
                    )
                )
                del self.triangles[i]
            else:
                self.triangles[i].x = new_mapping[self.triangles[i].x]
                self.triangles[i].y = new_mapping[self.triangles[i].y]
                self.triangles[i].z = new_mapping[self.triangles[i].z]

        return MeshDataItemTriangles(list(reversed(cut_triangles)))

    def paste(self, pasted_triangles: 'MeshDataItemTriangles', num_vertices: int):
        for i in range(len(pasted_triangles.triangles)):
            self.triangles.append(Int3(
                pasted_triangles.triangles[i].x + num_vertices,
                pasted_triangles.triangles[i].y + num_vertices,
                pasted_triangles.triangles[i].z + num_vertices
            ))

    def __str__(self) -> str:
        return "Num Triangles: " + str(len(self.triangles))

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshTriangles)
        writer.write_int(len(self.triangles) * 3)
        for triangle in self.triangles:
            writer.write_int3(triangle)

    @staticmethod
    def read_sub(reader: ByteReader) -> 'MeshDataItemTriangles':
        reader.read_int()  # Consume Tag
        num_triangles = reader.read_int()

        triangles = []
        for _ in range(num_triangles // 3):
            triangles.append(reader.read_int3())

        return MeshDataItemTriangles(
            triangles = triangles
        )


class MeshDataItemUvs(MeshDataItem):
    def __init__(self, uvs: list[Vec2], is_uv2: bool = False):
        self.uvs = uvs
        self.is_uv2 = is_uv2

    def cut(self, cut_indices: list[int]) -> 'MeshDataItemUvs':
        cut_uvs = []
        for i in reversed(range(len(self.uvs))):
            if i in cut_indices:
                cut_uvs.append(self.uvs[i])
                del self.uvs[i]

        return MeshDataItemUvs(list(reversed(cut_uvs)), self.is_uv2)

    def paste(self, pasted_uvs: 'MeshDataItemUvs'):
        for uv in pasted_uvs.uvs:
            self.uvs.append(uv)

    def write(self, writer: ByteWriter):
        if self.is_uv2:
            writer.write_int(MuTag.MeshUv2)
        else:
            writer.write_int(MuTag.MeshUv)

        for uv in self.uvs:
            writer.write_vec2(uv)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemUvs':
        is_uv2 = reader.read_int() == MuTag.MeshUv2

        uvs = []
        for _ in range(vertex_count):
            uvs.append(reader.read_vec2())

        return MeshDataItemUvs(
            uvs = uvs,
            is_uv2 = is_uv2
        )


class MeshDataItemVertexColors(MeshDataItem):
    def __init__(self, vertex_colors: list[ColorByte]):
        self.vertex_colors = vertex_colors

    def cut(self, cut_indices: list[int]) -> 'MeshDataItemVertexColors':
        cut_vertex_colors = []
        for i in reversed(range(len(self.vertex_colors))):
            if i in cut_indices:
                cut_vertex_colors.append(self.vertex_colors[i])
                del self.vertex_colors[i]

        return MeshDataItemVertexColors(list(reversed(cut_vertex_colors)))

    def paste(self, pasted_vertex_colors: 'MeshDataItemVertexColors'):
        for vertex_color in pasted_vertex_colors.vertex_colors:
            self.vertex_colors.append(vertex_color)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshVertexColors)
        for vertex in self.vertex_colors:
            writer.write_color_byte(vertex)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemVertexColors':
        reader.read_int()  # Consume Tag

        vertex_colors = []
        for _ in range(vertex_count):
            vertex_colors.append(reader.read_color_byte())

        return MeshDataItemVertexColors(
            vertex_colors = vertex_colors
        )


class MeshDataItemVertices(MeshDataItem):
    def __init__(self, vertices: list[Vec3]):
        self.vertices = vertices

    def cut(self, cut_indices: list[int]) -> 'MeshDataItemVertices':
        cut_vertices = []
        for i in reversed(range(len(self.vertices))):
            if i in cut_indices:
                cut_vertices.append(self.vertices[i])
                del self.vertices[i]

        return MeshDataItemVertices(list(reversed(cut_vertices)))

    def paste(self, pasted_vertices: 'MeshDataItemVertices'):
        for vertex in pasted_vertices.vertices:
            self.vertices.append(vertex)

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshVertices)
        for vertex in self.vertices:
            writer.write_vec3(vertex)

    @staticmethod
    def read_sub(reader: ByteReader, vertex_count: int) -> 'MeshDataItemVertices':
        reader.read_int()  # Consume Tag

        vertices = []
        for _ in range(vertex_count):
            vertices.append(reader.read_vec3())

        return MeshDataItemVertices(
            vertices = vertices
        )