import math

import moderngl
import numpy as np

from .mesh import Mesh
from .shader import Shader
from ..ecs.components import Sprite, Transform

# Shaders inline — mover para arquivos quando crescer
BASIC_VERT = """
#version 330 core
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_proj;

in vec3 in_position;

void main() {
    gl_Position = u_proj * u_view * u_model * vec4(in_position, 1.0);
}
"""

BASIC_FRAG = """
#version 330 core
uniform vec4 u_color;
out vec4 frag_color;

void main() {
    frag_color = u_color;
}
"""


class Renderer:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.shader = Shader(ctx, BASIC_VERT, BASIC_FRAG)
        self.quad = Mesh.quad(ctx, self.shader.program)

        self.view = np.eye(4, dtype="f4")
        self.proj = np.eye(4, dtype="f4")

    def set_camera(self, view: np.ndarray, proj: np.ndarray) -> None:
        self.view = view
        self.proj = proj

    def begin(self) -> None:
        self.ctx.clear(0.10, 0.10, 0.15, 1.0)

    def draw_world(self, world) -> None:
        self.shader.set_mat4("u_view", self.view)
        self.shader.set_mat4("u_proj", self.proj)

        for _, (t, s) in world.query(Transform, Sprite):
            model = self._model_matrix(t, s)
            self.shader.set_mat4("u_model", model)
            self.shader.set_vec4("u_color", (s.r, s.g, s.b, s.a))
            self.quad.render()

    @staticmethod
    def _model_matrix(t: Transform, s: Sprite) -> np.ndarray:
        # Quad unitário × (width, height) → sprite com aquele tamanho.
        c = math.cos(t.rot_z)
        sn = math.sin(t.rot_z)
        sx = s.width
        sy = s.height
        return np.array([
            [c * sx, -sn * sy, 0.0, t.x],
            [sn * sx,  c * sy, 0.0, t.y],
            [0.0,      0.0,    1.0, t.z],
            [0.0,      0.0,    0.0, 1.0],
        ], dtype="f4")