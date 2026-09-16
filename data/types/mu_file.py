from collections import deque
from pathlib import Path

from data.types.core.byte_reader import ByteReader
from data.types.core.byte_writer import ByteWriter
from data.types.material.material import Material
from data.types.material.material_property import MaterialProperty
from data.types.material.texture import Texture
from data.types.mu_tag import MuTag
from data.types.mu_transform import Transform
from data.types.transform.mesh.mesh_data import MeshData
from data.utils.errors import AttributeNotFoundError


class MuFile:
    def __init__(self, name: str, root_transform: Transform, materials: list[Material] | None = None, textures: list[Texture] | None = None):
        self.name = name

        self.root_transform = root_transform
        self.materials = [] if materials is None else materials
        self.textures = [] if textures is None else textures

    def __str__(self) -> str:
        return self.name

    def get_mesh(self, mesh_name: str) -> MeshData:
        queue: deque[Transform] = deque()
        queue.append(self.root_transform)

        while len(queue) > 0:
            transform: Transform = queue.pop()
            if transform.name == mesh_name:
                if transform.mesh_data is not None:
                    return transform.mesh_data
                break

            for child in transform.children:
                queue.append(child)

        raise AttributeNotFoundError(f'Transform with mesh data with name {mesh_name} not found in file')

    def get_material(self, material_name) -> Material:
        for material in self.materials:
            if material.name == material_name:
                return material

        raise AttributeNotFoundError(f'Material with name {material_name} not found in file')

    def get_material_index(self, material_name) -> int:
        for index, material in enumerate(self.materials):
            if material.name == material_name:
                return index

        raise AttributeNotFoundError(f'Material with name {material_name} not found in file')

    def get_property(self, material_name, property_name) -> MaterialProperty:
        material = self.get_material(material_name)
        for material_property in material.properties:
            if material_property.name == property_name:
                return material_property

    def get_texture_index(self, texture_name) -> int:
        for index, texture in enumerate(self.textures):
            if texture.name == texture_name:
                return index

        raise AttributeNotFoundError(f'Texture with name {texture_name} not found in file. Did you forget a file extension?')


    def write(self, writer: ByteWriter | None = None) -> bytes:
        # Allow passing in a custom writer for testing
        if writer is None:
            writer = ByteWriter()

        # Mu file identifier and version number
        writer.write_byte(0xFF)
        writer.write_byte(0x2A)
        writer.write_byte(0x01)
        writer.write_byte(0x00)
        writer.write_int(5)

        writer.write_str(self.name)

        self.root_transform.write(writer)

        if len(self.materials) > 0:
            writer.write_int(MuTag.Materials)
            writer.write_int(len(self.materials))
            for material in self.materials:
                material.write(writer)

        if len(self.textures) > 0:
            writer.write_int(MuTag.Textures)
            writer.write_int(len(self.textures))
            for texture in self.textures:
                texture.write(writer)

        return writer.output_data

    @staticmethod
    def read(reader: ByteReader) -> 'MuFile':
        # Skip Header
        reader.read_int()
        reader.read_int()

        name = reader.read_str()

        root_transform = Transform.read(reader)

        materials: list[Material] = []
        if reader.has_data() and reader.preview() == MuTag.Materials:
            reader.read_int()  # Consume the tag
            materials_count = reader.read_int()
            for i in range(materials_count):
                material = Material.read(reader)
                materials.append(material)

        textures: list[Texture] = []
        if reader.has_data() and reader.preview() == MuTag.Textures:
            reader.read_int()  # Consume the tag
            textures_count = reader.read_int()
            for i in range(textures_count):
                texture = Texture.read(reader)
                textures.append(texture)

        return MuFile(
            name = name,
            root_transform = root_transform,
            materials = materials,
            textures = textures
        )

    def write_file(self, filename: Path):
        output = self.write()
        with open(filename, "wb") as f:
            f.write(output)

    @staticmethod
    def read_file(filename: Path) -> 'MuFile':
        with open(filename, "rb") as f:
            data = f.read()

        reader = ByteReader(data)
        mu_file = MuFile.read(reader)
        return mu_file