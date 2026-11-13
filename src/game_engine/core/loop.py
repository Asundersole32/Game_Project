import time


class GameLoop:
    """
    Loop com fixed timestep para lógica e render livre.
    - update(dt) roda N vezes por frame com dt fixo (determinismo)
    - render(alpha) roda uma vez por frame; alpha é a interpolação
      entre o tick anterior e o próximo (para interpol. visual).
    - poll() deve retornar False para encerrar.
    """

    def __init__(self, update, render, poll, ups: int = 60):
        self.update = update
        self.render = render
        self.poll = poll
        self.ups = ups
        self.dt = 1.0 / ups
        self.running = False
        self._accumulator = 0.0

    def run(self) -> None:
        self.running = True
        last = time.perf_counter()

        while self.running:
            if not self.poll():
                break

            now = time.perf_counter()
            frame_time = min(now - last, 0.25)  # clamp anti "espiral da morte"
            last = now
            self._accumulator += frame_time

            while self._accumulator >= self.dt:
                self.update(self.dt)
                self._accumulator -= self.dt

            alpha = self._accumulator / self.dt
            self.render(alpha)

    def stop(self) -> None:
        self.running = False