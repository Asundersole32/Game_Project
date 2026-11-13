from dataclasses import dataclass


@dataclass
class Transform:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rot_z: float = 0.0  # radianos, rotação no plano XY


@dataclass
class Velocity:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Sprite:
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    width: float = 1.0
    height: float = 1.0