from data.types.core.byte_reader import ByteReader
from data.types.core.byte_writer import ByteWriter
from data.types.transform.mesh.mesh_data_item import MeshDataItem
from data.types.transform.mesh.mesh_renderer_settings import MeshRendererSettings
from data.types.mu_tag import MuTag


class MeshData:
    def __init__(self,
                 vertex_count: int,
                 submesh_count: int,
                 items: dict[MuTag, MeshDataItem] | None = None,
                 render_settings: MeshRendererSettings | None = None):
        self.vertex_count = vertex_count
        self.submesh_count = submesh_count

        # Preserver tag order
        self.items = items if items is not None else {}

        self.render_settings: MeshRendererSettings | None = render_settings

    def __str__(self) -> str:
        return f"Mesh Data (Vertices: {self.vertex_count})"

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.MeshStart)
        writer.write_int(self.vertex_count)
        writer.write_int(self.submesh_count)

        for item in self.items.values():
            item.write(writer)

        writer.write_int(MuTag.MeshEnd)

        if self.render_settings is not None:
            self.render_settings.write(writer)

    @staticmethod
    def read(reader: ByteReader) -> MeshData:
        reader.read_int()  # Consume MeshStart Tag
        vertex_count = reader.read_int()
        submesh_count = reader.read_int()

        items = {}
        while reader.preview() != MuTag.MeshEnd:
            tag = reader.preview()
            item = MeshDataItem.read(reader, vertex_count)
            items[tag] = item

        reader.read_int()  # Consume MeshEnd Tag
        render_settings = MeshRendererSettings.read(reader) if reader.preview() == MuTag.MeshRenderer else None

        return MeshData(
            vertex_count = vertex_count,
            submesh_count = submesh_count,
            items = items,
            render_settings = render_settings
        )