import numpy as np


def perspective(fov_deg: float, aspect: float, near: float, far: float) -> np.ndarray:
    f = 1.0 / np.tan(np.radians(fov_deg) / 2.0)
    m = np.zeros((4, 4), dtype="f4")
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2 * far * near) / (near - far)
    m[3, 2] = -1.0
    return m


def ortho(left, right, bottom, top, near, far) -> np.ndarray:
    m = np.zeros((4, 4), dtype="f4")
    m[0, 0] = 2.0 / (right - left)
    m[1, 1] = 2.0 / (top - bottom)
    m[2, 2] = -2.0 / (far - near)
    m[0, 3] = -(right + left) / (right - left)
    m[1, 3] = -(top + bottom) / (top - bottom)
    m[2, 3] = -(far + near) / (far - near)
    m[3, 3] = 1.0
    return m


def look_at(eye, target, up) -> np.ndarray:
    eye = np.array(eye, dtype="f4")
    target = np.array(target, dtype="f4")
    up = np.array(up, dtype="f4")

    f = target - eye
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)

    m = np.eye(4, dtype="f4")
    m[0, :3] = s
    m[1, :3] = u
    m[2, :3] = -f
    m[0, 3] = -np.dot(s, eye)
    m[1, 3] = -np.dot(u, eye)
    m[2, 3] = np.dot(f, eye)
    return m


class Camera:
    """Câmera orbital e free-fly (alterna com F). Suporta persp e ortho."""

    def __init__(self):
        self.target = np.array([0.0, 0.0, 0.0], dtype="f4")
        self.distance = 8.0
        self.yaw = 0.0
        self.pitch = 0.35
        self.fov = 60.0
        self.near = 0.1
        self.far = 200.0
        self.mode = "persp"
        self.ortho_size = 4.0

        self.fly = False
        self.fly_position = np.array([0.0, 2.0, 6.0], dtype="f4")

    def position(self) -> np.ndarray:
        if self.fly:
            return self.fly_position.copy()
        cp = np.cos(self.pitch)
        return np.array([
            self.target[0] + self.distance * cp * np.sin(self.yaw),
            self.target[1] + self.distance * np.sin(self.pitch),
            self.target[2] + self.distance * cp * np.cos(self.yaw),
        ], dtype="f4")

    def forward(self) -> np.ndarray:
        cp = np.cos(self.pitch)
        return np.array([
            -cp * np.sin(self.yaw),
            np.sin(self.pitch),
            -cp * np.cos(self.yaw),
        ], dtype="f4")

    def right(self) -> np.ndarray:
        return np.array([np.cos(self.yaw), 0.0, -np.sin(self.yaw)], dtype="f4")

    def forward_xy(self) -> np.ndarray:
        return np.array([-np.sin(self.yaw), 0.0, -np.cos(self.yaw)], dtype="f4")

    def right_xy(self) -> np.ndarray:
        return np.array([np.cos(self.yaw), 0.0, -np.sin(self.yaw)], dtype="f4")

    def view(self) -> np.ndarray:
        eye = self.position()
        if self.fly:
            target = eye + self.forward()
        else:
            target = self.target
        return look_at(eye, target, (0.0, 1.0, 0.0))

    def proj(self, aspect: float) -> np.ndarray:
        if self.mode == "persp":
            return perspective(self.fov, aspect, self.near, self.far)
        h = self.ortho_size
        w = h * aspect
        return ortho(-w, w, -h, h, self.near, self.far)

    def toggle_mode(self) -> None:
        if self.mode == "persp":
            self.ortho_size = self.distance * np.tan(np.radians(self.fov) / 2.0)
            self.mode = "ortho"
        else:
            self.distance = self.ortho_size / np.tan(np.radians(self.fov) / 2.0)
            self.mode = "persp"