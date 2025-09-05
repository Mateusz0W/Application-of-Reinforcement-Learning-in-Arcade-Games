import build.Debug.DonkeyKongPy as DK
jm = DK.Jumpman() 
sim = DK.Simulation(jm,1700,1500,False)
sim.loadMapFromJson("map.json")
renderer = DK.Renderer(sim,1700,1500)
while renderer.isOpen():
    done = bool(sim.run())
    a = sim.getBarrelsPositions()
    b = sim.getJumpmanPosition()
    renderer.run()
    print(done)