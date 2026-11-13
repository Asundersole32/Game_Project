# engine/render/shader.py
import moderngl
import numpy as np


class Shader:
    def __init__(self, ctx: moderngl.Context, vert_src: str, frag_src: str):
        self.program = ctx.program(
            vertex_shader=vert_src,
            fragment_shader=frag_src,
        )

    # use() removido — o VAO já vincula o programa no render()

    def set_mat4(self, name: str, mat: np.ndarray) -> None:
        self.program[name].write(mat.astype("f4").T.tobytes())

    def set_vec4(self, name: str, v) -> None:
        self.program[name].value = tuple(v)