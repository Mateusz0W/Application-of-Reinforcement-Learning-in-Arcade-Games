import build.Debug.DonkeyKongPy as DK
jm = DK.Jumpman() 
sim = DK.Simulation(jm,1700,1500)
sim.loadMapFromJson("map.json")
renderer = DK.Renderer(sim,1700,1500)
renderer.run()