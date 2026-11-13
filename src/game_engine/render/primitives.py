import numpy as np


def _to_bytes(verts, idx):
    return (np.array(verts, dtype="f4").tobytes(),
            np.array(idx, dtype="i4").tobytes())


def cube():
    """Cubo unitário [-0.5, 0.5]^3, normais por face, UVs simples."""
    vertices = [
        # +X
         0.5, -0.5, -0.5,  1, 0, 0,  1, 0,
         0.5,  0.5, -0.5,  1, 0, 0,  1, 1,
         0.5,  0.5,  0.5,  1, 0, 0,  0, 1,
         0.5, -0.5,  0.5,  1, 0, 0,  0, 0,
        # -X
        -0.5, -0.5,  0.5, -1, 0, 0,  1, 0,
        -0.5,  0.5,  0.5, -1, 0, 0,  1, 1,
        -0.5,  0.5, -0.5, -1, 0, 0,  0, 1,
        -0.5, -0.5, -0.5, -1, 0, 0,  0, 0,
        # +Y
        -0.5,  0.5, -0.5,  0, 1, 0,  1, 0,
        -0.5,  0.5,  0.5,  0, 1, 0,  1, 1,
         0.5,  0.5,  0.5,  0, 1, 0,  0, 1,
         0.5,  0.5, -0.5,  0, 1, 0,  0, 0,
        # -Y
        -0.5, -0.5,  0.5,  0,-1, 0,  1, 0,
        -0.5, -0.5, -0.5,  0,-1, 0,  1, 1,
         0.5, -0.5, -0.5,  0,-1, 0,  0, 1,
         0.5, -0.5,  0.5,  0,-1, 0,  0, 0,
        # +Z
        -0.5, -0.5,  0.5,  0, 0, 1,  1, 0,
         0.5, -0.5,  0.5,  0, 0, 1,  1, 1,
         0.5,  0.5,  0.5,  0, 0, 1,  0, 1,
        -0.5,  0.5,  0.5,  0, 0, 1,  0, 0,
        # -Z
         0.5, -0.5, -0.5,  0, 0,-1,  1, 0,
        -0.5, -0.5, -0.5,  0, 0,-1,  1, 1,
        -0.5,  0.5, -0.5,  0, 0,-1,  0, 1,
         0.5,  0.5, -0.5,  0, 0,-1,  0, 0,
    ]
    indices = []
    for face in range(6):
        b = face * 4
        indices += [b, b + 1, b + 2, b, b + 2, b + 3]
    return _to_bytes(vertices, indices)


def sphere(lat_segments: int = 24, lon_segments: int = 48):
    """Esfera UV de raio 1."""
    verts = []
    for i in range(lat_segments + 1):
        theta = i * np.pi / lat_segments
        sin_t = np.sin(theta)
        cos_t = np.cos(theta)
        for j in range(lon_segments + 1):
            phi = j * 2 * np.pi / lon_segments
            x = sin_t * np.cos(phi)
            y = cos_t
            z = sin_t * np.sin(phi)
            u = j / lon_segments
            v = i / lat_segments
            verts += [x, y, z, x, y, z, u, v]

    idx = []
    for i in range(lat_segments):
        for j in range(lon_segments):
            a = i * (lon_segments + 1) + j
            b = a + lon_segments + 1
            idx += [a, b, a + 1, a + 1, b, b + 1]
    return _to_bytes(verts, idx)


def plane():
    """Plano unitário no plano XZ (normal +Y)."""
    vertices = [
        -0.5, 0, -0.5,  0, 1, 0,  0, 0,
         0.5, 0, -0.5,  0, 1, 0,  1, 0,
         0.5, 0,  0.5,  0, 1, 0,  1, 1,
        -0.5, 0,  0.5,  0, 1, 0,  0, 1,
    ]
    indices = [0, 1, 2, 0, 2, 3]
    return _to_bytes(vertices, indices)