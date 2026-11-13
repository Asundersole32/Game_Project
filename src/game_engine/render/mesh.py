import moderngl
import numpy as np


class Mesh:
    def __init__(self, ctx: moderngl.Context, program, vertices: bytes, layout: str, indices: bytes | None = None):
        self.ctx = ctx
        self.vbo = ctx.buffer(vertices)
        self.ibo = ctx.buffer(indices) if indices is not None else None
        self.vao = ctx.vertex_array(
            program,
            [(self.vbo, layout, "in_position")],
            self.ibo,
        )

    def render(self) -> None:
        self.vao.render(moderngl.TRIANGLES)

    @classmethod
    def quad(cls, ctx: moderngl.Context, program) -> "Mesh":
        # Quad unitário 1x1 centrado na origem, no plano XY (Z=0)
        vertices = np.array([
            -0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.5,  0.5, 0.0,
            -0.5,  0.5, 0.0,
        ], dtype="f4").tobytes()
        indices = np.array([0, 1, 2, 0, 2, 3], dtype="i4").tobytes()
        return cls(ctx, program, vertices, "3f", indices)