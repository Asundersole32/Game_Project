import moderngl
import numpy as np

from .camera import Camera
from .mesh import InstancedMesh, InstancedQuad
from .primitives import cube, plane, sphere
from .shader import Shader
from .texture import white_texture
from ..ecs.components import MeshRenderer, Sprite, Transform


MESH_VERT = """
#version 330 core
uniform mat4 u_view;
uniform mat4 u_proj;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

in vec4 in_col0;
in vec4 in_col1;
in vec4 in_col2;
in vec4 in_col3;
in vec4 in_color;

out vec3 v_world_pos;
out vec3 v_world_normal;
out vec2 v_uv;
out vec4 v_color;

void main() {
    mat4 model = mat4(in_col0, in_col1, in_col2, in_col3);
    vec4 wp = model * vec4(in_position, 1.0);
    v_world_pos = wp.xyz;
    v_world_normal = mat3(model) * in_normal;
    v_uv = in_uv;
    v_color = in_color;
    gl_Position = u_proj * u_view * wp;
}
"""

MESH_FRAG = """
#version 330 core
uniform sampler2D u_texture;
uniform vec3 u_light_dir;
uniform vec3 u_light_color;
uniform vec3 u_ambient_color;
uniform vec3 u_camera_pos;

in vec3 v_world_pos;
in vec3 v_world_normal;
in vec2 v_uv;
in vec4 v_color;
out vec4 frag_color;

void main() {
    vec3 N = normalize(v_world_normal);
    vec3 L = normalize(u_light_dir);
    vec3 V = normalize(u_camera_pos - v_world_pos);
    vec3 H = normalize(L + V);

    float diff = max(dot(N, L), 0.0);
    float spec = pow(max(dot(N, H), 0.0), 32.0) * 0.35;

    vec3 base = texture(u_texture, v_uv).rgb * v_color.rgb;
    vec3 color = base * (u_ambient_color + u_light_color * diff) + u_light_color * spec;
    frag_color = vec4(color, v_color.a);
}
"""

SPRITE_VERT = """
#version 330 core
uniform mat4 u_view;
uniform mat4 u_proj;

in vec3 in_position;
in vec2 in_uv;

in vec4 in_instance_pos_rot;
in vec4 in_instance_scale;
in vec4 in_instance_color;

out vec2 v_uv;
out vec4 v_color;

void main() {
    float c = cos(in_instance_pos_rot.w);
    float s = sin(in_instance_pos_rot.w);
    vec2 scaled = in_position.xy * in_instance_scale.xy;
    vec2 rotated = vec2(
        c * scaled.x - s * scaled.y,
        s * scaled.x + c * scaled.y
    );
    vec3 world = vec3(rotated + in_instance_pos_rot.xy, in_instance_pos_rot.z);
    gl_Position = u_proj * u_view * vec4(world, 1.0);
    v_uv = in_uv;
    v_color = in_instance_color;
}
"""

SPRITE_FRAG = """
#version 330 core
uniform sampler2D u_texture;
in vec2 v_uv;
in vec4 v_color;
out vec4 frag_color;
void main() {
    frag_color = texture(u_texture, v_uv) * v_color;
}
"""


def _transform_matrix(t: Transform) -> np.ndarray:
    cosx, sinx = np.cos(t.rx), np.sin(t.rx)
    cosy, siny = np.cos(t.ry), np.sin(t.ry)
    cosz, sinz = np.cos(t.rz), np.sin(t.rz)

    rx = np.array([[1, 0, 0], [0, cosx, -sinx], [0, sinx, cosx]], dtype="f4")
    ry = np.array([[cosy, 0, siny], [0, 1, 0], [-siny, 0, cosy]], dtype="f4")
    rz = np.array([[cosz, -sinz, 0], [sinz, cosz, 0], [0, 0, 1]], dtype="f4")

    m = np.eye(4, dtype="f4")
    m[:3, :3] = (rz @ ry @ rx) @ np.diag([t.sx, t.sy, t.sz]).astype("f4")
    m[:3, 3] = (t.x, t.y, t.z)
    return m


class Renderer:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx

        # 3D
        self.shader_3d = Shader(ctx, MESH_VERT, MESH_FRAG)
        self.meshes: dict[str, InstancedMesh] = {}
        self._register_mesh("cube", *cube())
        self._register_mesh("sphere", *sphere())
        self._register_mesh("plane", *plane())

        # 2D
        self.shader_2d = Shader(ctx, SPRITE_VERT, SPRITE_FRAG)
        self.quad_2d = InstancedQuad(ctx, self.shader_2d.program)

        # Texturas
        self.textures: dict[str, moderngl.Texture] = {"white": white_texture(ctx)}

        # Luz
        d = np.array([0.5, 1.0, 0.4], dtype="f4")
        self.light_dir = d / np.linalg.norm(d)
        self.light_color = np.array([1.0, 0.95, 0.85], dtype="f4")
        self.ambient_color = np.array([0.20, 0.22, 0.30], dtype="f4")

        self._camera_pos = np.zeros(3, dtype="f4")

        ctx.enable(moderngl.BLEND)
        ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        ctx.enable(moderngl.DEPTH_TEST)
        ctx.disable(moderngl.CULL_FACE)  # winding não verificado ainda

    def _register_mesh(self, name: str, vertices: bytes, indices: bytes) -> None:
        self.meshes[name] = InstancedMesh(
            self.ctx, self.shader_3d.program, vertices, indices
        )

    def register_texture(self, name: str, tex: moderngl.Texture) -> None:
        self.textures[name] = tex

    def begin(self) -> None:
        self.ctx.clear(0.10, 0.10, 0.15, 1.0, depth=1.0)

    def draw_world(self, world, camera: Camera, aspect: float) -> None:
        self._camera_pos[:] = camera.position()
        view = camera.view()
        proj = camera.proj(aspect)

        self._draw_meshes_3d(world, view, proj)

        self.ctx.disable(moderngl.DEPTH_TEST)
        try:
            self._draw_sprites_2d(world, view, proj)
        finally:
            self.ctx.enable(moderngl.DEPTH_TEST)

    def _draw_meshes_3d(self, world, view, proj) -> None:
        prog = self.shader_3d.program
        self.shader_3d.set_mat4("u_view", view)
        self.shader_3d.set_mat4("u_proj", proj)
        prog["u_light_dir"].value = tuple(self.light_dir)
        prog["u_light_color"].value = tuple(self.light_color)
        prog["u_ambient_color"].value = tuple(self.ambient_color)
        prog["u_camera_pos"].value = tuple(self._camera_pos)
        prog["u_texture"].value = 0

        groups: dict[tuple[str, str], list] = {}
        for _, (t, m) in world.query(Transform, MeshRenderer):
            groups.setdefault((m.mesh_id, m.texture_id), []).append((t, m))

        for (mesh_id, tex_id), items in groups.items():
            mesh = self.meshes.get(mesh_id)
            if mesh is None:
                continue
            tex = self.textures.get(tex_id) or self.textures["white"]
            tex.use(0)

            n = len(items)
            matrices = np.empty((n, 4, 4), dtype="f4")
            colors = np.empty((n, 4), dtype="f4")
            for i, (t, m) in enumerate(items):
                matrices[i] = _transform_matrix(t)
                colors[i] = (m.r, m.g, m.b, m.a)
            mesh.render(matrices, colors)

    def _draw_sprites_2d(self, world, view, proj) -> None:
        self.shader_2d.set_mat4("u_view", view)
        self.shader_2d.set_mat4("u_proj", proj)
        self.shader_2d.program["u_texture"].value = 0

        groups: dict[str, list] = {}
        for _, (t, s) in world.query(Transform, Sprite):
            groups.setdefault(s.texture_id, []).append((t, s))

        for tex_id, sprites in groups.items():
            tex = self.textures.get(tex_id) or self.textures["white"]
            tex.use(0)

            n = len(sprites)
            data = np.empty((n, 10), dtype="f4")
            for i, (t, s) in enumerate(sprites):
                data[i, 0] = t.x
                data[i, 1] = t.y
                data[i, 2] = t.z
                data[i, 3] = t.rz
                data[i, 4] = s.width * t.sx
                data[i, 5] = s.height * t.sy
                data[i, 6] = s.r
                data[i, 7] = s.g
                data[i, 8] = s.b
                data[i, 9] = s.a
            self.quad_2d.render(data)