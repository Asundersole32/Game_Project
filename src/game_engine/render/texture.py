import moderngl
import numpy as np

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def load_texture(ctx: moderngl.Context, path: str) -> moderngl.Texture:
    """Carrega PNG/JPG via Pillow. Origem em bottom-left (OpenGL)."""
    if not HAS_PIL:
        raise ImportError("Pillow é necessário para carregar imagens: pip install Pillow")
    img = Image.open(path).convert("RGBA")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    tex = ctx.texture(img.size, 4, img.tobytes())
    tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
    tex.build_mipmaps()
    return tex


def checkerboard(
    ctx: moderngl.Context,
    size: int = 64,
    squares: int = 8,
    c1: tuple = (255, 255, 255),
    c2: tuple = (60, 60, 80),
) -> moderngl.Texture:
    """Textura procedural (sem dependência de asset)."""
    cell = max(1, size // squares)
    x = np.arange(size)
    y = np.arange(size)
    xx, yy = np.meshgrid(x, y)
    mask = ((xx // cell) + (yy // cell)) % 2 == 0
    arr = np.zeros((size, size, 4), dtype="u1")
    arr[mask] = (*c1, 255)
    arr[~mask] = (*c2, 255)
    tex = ctx.texture((size, size), 4, arr.tobytes())
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    return tex


def white_texture(ctx: moderngl.Context) -> moderngl.Texture:
    """Textura branca 1x1 — permite colorir sprites sem imagem."""
    arr = np.array([[[255, 255, 255, 255]]], dtype="u1")
    tex = ctx.texture((1, 1), 4, arr.tobytes())
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    return tex