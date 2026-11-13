from dataclasses import dataclass


@dataclass
class Transform:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rx: float = 0.0  # rotação X (radianos)
    ry: float = 0.0  # rotação Y
    rz: float = 0.0  # rotação Z (usado por sprites 2D)
    sx: float = 1.0
    sy: float = 1.0
    sz: float = 1.0


@dataclass
class Velocity:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class MeshRenderer:
    """Renderiza uma malha 3D iluminada."""
    mesh_id: str = "cube"
    texture_id: str = "white"
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0


@dataclass
class Sprite:
    """Renderiza um quad 2D (não iluminado, desenhado por cima)."""
    texture_id: str = "white"
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    width: float = 1.0
    height: float = 1.0


@dataclass
class Spin:
    speed: float = 1.5
    axis: str = "y"  # "x" | "y" | "z"