import sdl2

from src.game_engine.core.app import App
from src.game_engine.ecs.components import Sprite, Transform, Velocity
from src.game_engine.ecs.systems import movement_system, spin_system


def main() -> None:
    app = App(title="Python Engine — Fase 0", width=1280, height=720)

    # Entidade A: move para a direita
    a = app.world.create()
    app.world.add(a, Transform(x=-1.5, y=0.0, z=0.0))
    app.world.add(a, Velocity(x=0.6, y=0.0, z=0.0))
    app.world.add(a, Sprite(r=1.0, g=0.35, b=0.25, width=0.5, height=0.5))

    # Entidade B: estática
    b = app.world.create()
    app.world.add(b, Transform(x=1.2, y=0.6, z=0.0))
    app.world.add(b, Sprite(r=0.3, g=0.7, b=1.0, width=0.8, height=0.8))

    # Entidade C: rotacionando (segure R para inverter)
    c = app.world.create()
    app.world.add(c, Transform(x=0.0, y=-1.0, z=0.0))
    app.world.add(c, Sprite(r=0.5, g=1.0, b=0.4, width=0.4, height=0.4))

    app.add_system(movement_system)
    app.add_system(spin_system)

    app.run()


if __name__ == "__main__":
    main()