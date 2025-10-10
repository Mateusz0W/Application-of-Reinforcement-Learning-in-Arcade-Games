from simulation import Simulation
from renderer import Renderer


if __name__ == "__main__":
    sim = Simulation()
    renderer = Renderer()
    running = True
    while running:
        sim.run()
        running = renderer.render(sim, running)