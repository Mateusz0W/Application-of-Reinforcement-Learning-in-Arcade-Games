import build.Debug.DonkeyKongPy as DK
jm = DK.Jumpman() 
sim = DK.Simulation(jm,1500,1700)
sim.loadMapFromJson("map.json")
renderer = DK.Renderer(sim,1500,1700)
renderer.run()