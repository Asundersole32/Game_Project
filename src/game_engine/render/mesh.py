import moderngl
import numpy as np


class InstancedMesh:
    """
    Malha 3D com instancing.
    Layout de vértice: position(3f) + normal(3f) + uv(2f) = 32 bytes.
    Layout de instância: matriz 4x4 (4 vec4) + cor (vec4) = 80 bytes.
    Buffers de instância separados por atributo (uniform '4f/i').
    """

    def __init__(self, ctx: moderngl.Context, program,
                 vertices: bytes, indices: bytes, max_instances: int = 8192):
        self.max_instances = max_instances
        self.vbo = ctx.buffer(vertices)
        self.ibo = ctx.buffer(indices)

        reserve = max_instances * 16  # 16 bytes por vec4 por instância
        self.col_bufs = [ctx.buffer(reserve=reserve) for _ in range(4)]
        self.color_buf = ctx.buffer(reserve=reserve)

        self.vao = ctx.vertex_array(
            program,
            [
                (self.vbo, "3f 3f 2f", "in_position", "in_normal", "in_uv"),
                (self.col_bufs[0], "4f/i", "in_col0"),
                (self.col_bufs[1], "4f/i", "in_col1"),
                (self.col_bufs[2], "4f/i", "in_col2"),
                (self.col_bufs[3], "4f/i", "in_col3"),
                (self.color_buf, "4f/i", "in_color"),
            ],
            self.ibo,
        )

    def render(self, matrices: np.ndarray, colors: np.ndarray) -> None:
        """matrices: (N, 4, 4) float32 — cores: (N, 4) float32."""
        n = matrices.shape[0]
        if n == 0:
            return
        if n > self.max_instances:
            raise RuntimeError(
                f"InstancedMesh: {n} instâncias excede max={self.max_instances}"
            )
        for i in range(4):
            col = np.ascontiguousarray(matrices[:, :, i], dtype="f4")
            self.col_bufs[i].write(col.tobytes())
        self.color_buf.write(np.ascontiguousarray(colors, dtype="f4").tobytes())
        self.vao.render(moderngl.TRIANGLES, instances=n)


class InstancedQuad:
    """Quad 2D com instancing (pos+rot+scale+color). Usado por Sprite."""

    def __init__(self, ctx: moderngl.Context, program, max_instances: int = 4096):
        vertices = np.array([
            -0.5, -0.5, 0.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.0, 1.0, 1.0,
            -0.5,  0.5, 0.0, 0.0, 1.0,
        ], dtype="f4").tobytes()
        indices = np.array([0, 1, 2, 0, 2, 3], dtype="i4").tobytes()

        self.vbo = ctx.buffer(vertices)
        self.ibo = ctx.buffer(indices)
        reserve = max_instances * 16
        self.posrot_buf = ctx.buffer(reserve=reserve)
        self.scale_buf = ctx.buffer(reserve=reserve)
        self.color_buf = ctx.buffer(reserve=reserve)

        self.vao = ctx.vertex_array(
            program,
            [
                (self.vbo, "3f 2f", "in_position", "in_uv"),
                (self.posrot_buf, "4f/i", "in_instance_pos_rot"),
                (self.scale_buf, "4f/i", "in_instance_scale"),
                (self.color_buf, "4f/i", "in_instance_color"),
            ],
            self.ibo,
        )

    def render(self, instance_data: np.ndarray) -> None:
        n = instance_data.shape[0]
        if n == 0:
            return
        posrot = np.ascontiguousarray(instance_data[:, 0:4], dtype="f4")
        scale = np.zeros((n, 4), dtype="f4")
        scale[:, 0:2] = instance_data[:, 4:6]
        color = np.ascontiguousarray(instance_data[:, 6:10], dtype="f4")
        self.posrot_buf.write(posrot.tobytes())
        self.scale_buf.write(scale.tobytes())
        self.color_buf.write(color.tobytes())
        self.vao.render(moderngl.TRIANGLES, instances=n)