from .components import Transform, Velocity


def movement_system(app, dt: float) -> None:
    """Integra Velocity em Transform."""
    for _, (t, v) in app.world.query(Transform, Velocity):
        t.x += v.x * dt
        t.y += v.y * dt
        t.z += v.z * dt


def spin_system(app, dt: float) -> None:
    """Roda entidades com Transform (demo)."""
    import sdl2
    speed = 1.5
    direction = 1.0 if not app.input.is_down(sdl2.SDLK_r) else -1.0
    for _, (t,) in app.world.query(Transform):
        t.rot_z += speed * direction * dt