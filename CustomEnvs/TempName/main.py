from simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(render=True)
    running = True
    while running:
        running = sim.run()