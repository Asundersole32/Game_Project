import numpy as np
import sdl2

from .components import Spin, Transform, Velocity


def movement_system(app, dt: float) -> None:
    for _, (t, v) in app.world.query(Transform, Velocity):
        t.x += v.x * dt
        t.y += v.y * dt
        t.z += v.z * dt


def spin_system(app, dt: float) -> None:
    for _, (t, s) in app.world.query(Transform, Spin):
        if s.axis == "x":
            t.rx += s.speed * dt
        elif s.axis == "y":
            t.ry += s.speed * dt
        else:
            t.rz += s.speed * dt


def camera_controller_system(app, dt: float) -> None:
    cam = app.camera
    inp = app.input

    # Alterna fly
    if inp.just_pressed(sdl2.SDLK_f):
        if cam.fly:
            cam.fly = False
            cam.target = cam.fly_position + cam.forward() * 4.0
        else:
            cam.fly_position = cam.position()
            cam.fly = True

    # Movimento
    if cam.fly:
        speed = 8.0
        fwd = cam.forward()
        rgt = cam.right()
        up = np.array([0.0, 1.0, 0.0], dtype="f4")
        move = np.zeros(3, dtype="f4")
        if inp.is_down(sdl2.SDLK_w): move += fwd
        if inp.is_down(sdl2.SDLK_s): move -= fwd
        if inp.is_down(sdl2.SDLK_d): move += rgt
        if inp.is_down(sdl2.SDLK_a): move -= rgt
        if inp.is_down(sdl2.SDLK_SPACE): move += up
        if inp.is_down(sdl2.SDLK_LCTRL): move -= up
        n = np.linalg.norm(move)
        if n > 0:
            cam.fly_position += (move / n) * speed * dt
    else:
        speed = 6.0 * max(1.0, cam.distance * 0.3)
        fwd = cam.forward_xy()
        rgt = cam.right_xy()
        if inp.is_down(sdl2.SDLK_w): cam.target += fwd * speed * dt
        if inp.is_down(sdl2.SDLK_s): cam.target -= fwd * speed * dt
        if inp.is_down(sdl2.SDLK_d): cam.target += rgt * speed * dt
        if inp.is_down(sdl2.SDLK_a): cam.target -= rgt * speed * dt

    # Mouse look
    if inp.is_mouse_down(sdl2.SDL_BUTTON_RIGHT):
        cam.yaw -= inp.mouse_dx * 0.005
        cam.pitch = float(np.clip(
            cam.pitch + inp.mouse_dy * 0.005,
            -1.5, 1.5,
        ))

    # Zoom orbital
    if not cam.fly and inp.wheel != 0:
        if cam.mode == "persp":
            cam.distance = max(0.5, cam.distance - inp.wheel * 0.5)
        else:
            cam.ortho_size = max(0.5, cam.ortho_size - inp.wheel * 0.5)