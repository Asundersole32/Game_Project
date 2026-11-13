from src.game_engine.core.app import App
from src.game_engine.ecs.components import MeshRenderer, Spin, Sprite, Transform, Velocity
from src.game_engine.ecs.systems import (
    camera_controller_system,
    movement_system,
    spin_system,
)
from src.game_engine.render.texture import checkerboard


def main() -> None:
    app = App(title="Python Engine — Fase 2 (3D)", width=1280, height=720)
    ctx = app.window.ctx

    app.renderer.register_texture("checker", checkerboard(ctx, size=64, squares=8))

    # Chão
    g = app.world.create()
    app.world.add(g, Transform(0, 0, 0, sx=20, sy=1, sz=20))
    app.world.add(g, MeshRenderer(mesh_id="plane", texture_id="checker",
                                  r=0.5, g=0.5, b=0.55))

    # Grid de cubos girando no eixo Y
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i == 0 and j == 0:
                continue
            e = app.world.create()
            app.world.add(e, Transform(
                x=i * 1.6, y=0.4, z=j * 1.6,
                sx=0.8, sy=0.8, sz=0.8,
            ))
            app.world.add(e, MeshRenderer(
                mesh_id="cube", texture_id="white",
                r=1.0, g=0.65, b=0.25,
            ))
            app.world.add(e, Spin(speed=0.8 + 0.15 * (i + j), axis="y"))

    # Esfera girando no centro (rotação mista)
    s = app.world.create()
    app.world.add(s, Transform(x=0.0, y=1.1, z=0.0, sx=0.7, sy=0.7, sz=0.7))
    app.world.add(s, MeshRenderer(
        mesh_id="sphere", texture_id="checker",
        r=0.4, g=0.85, b=1.0,
    ))
    app.world.add(s, Spin(speed=1.5, axis="y"))

    # Cubo orbitando a esfera (mostra transform 3D em movimento)
    o = app.world.create()
    app.world.add(o, Transform(x=2.5, y=1.1, z=0.0, sx=0.4, sy=0.4, sz=0.4))
    app.world.add(o, MeshRenderer(mesh_id="cube", texture_id="white",
                                  r=0.9, g=0.3, b=0.9))
    app.world.add(o, Spin(speed=2.0, axis="y"))

    # Sprite 2D flutuando (prova que o caminho 2D ainda funciona em cena 3D)
    sp = app.world.create()
    app.world.add(sp, Transform(x=0.0, y=3.0, z=0.0))
    app.world.add(sp, Sprite(texture_id="white", r=1.0, g=0.3, b=0.3,
                             width=0.8, height=0.8))
    # Sprite 2D movendo lateralmente
    mv = app.world.create()
    app.world.add(mv, Transform(x=-4.0, y=3.0, z=0.0))
    app.world.add(mv, Velocity(x=1.0, y=0.0, z=0.0))
    app.world.add(mv, Sprite(texture_id="white", r=0.3, g=1.0, b=0.3,
                             width=0.6, height=0.6))

    app.add_system(camera_controller_system)
    app.add_system(movement_system)
    app.add_system(spin_system)

    app.run()


if __name__ == "__main__":
    main()