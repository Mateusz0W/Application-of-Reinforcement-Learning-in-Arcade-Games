import build.Debug.DonkeyKongPy as DK

stages = {
    "1": [1116, False],
    "2": [894, False],
    "3": [674, False],
    "4": [454, False],
    "5": [234, False]
}

def _reach_next_stage(stages,y_pos):
    reward = 0
    for key in stages:
        if y_pos < stages[key][0] and not stages[key][1]:
            reward = 20
            stages[key][1] = True
            break

    return reward

def get_reward(simulation,prev_distance,jumpman):
    reward = 0
    princess_position = (450,70)
    jumpman_position = simulation.getJumpmanPosition()
    distance_y = abs(princess_position[1] - jumpman_position[1])
    distance_x = abs(princess_position[0] - jumpman_position[0])
    # if distance_y < prev_distance[1] and not jumpman.jumping:  
    #     reward += 10
    if distance_y > prev_distance[1] and not jumpman.fallingAfterJump and not jumpman.jumping:  
        reward -=5
    # if distance_x < prev_distance[0]:  
    #     reward += 0.1
    if simulation.getReset():
        reward -= 50
    if simulation.getWin():
        reward += 100
    reward += _reach_next_stage(stages,simulation.getJumpmanPosition()[1])

    return reward,(distance_x,distance_y)

actions = ["Jump","Right","Left","Up","Down"]

jm = DK.Jumpman() 
sim = DK.Simulation(jm,1700,1500,True)
sim.loadMapFromJson("map.json")
renderer = DK.Renderer(sim,1700,1500)
dist = sim.getJumpmanPosition()
reward = 0
i = 0
while renderer.isOpen():
    #sim.action = actions[i]
    done = bool(sim.run())
    a = sim.getBarrelsPositions()
    b = sim.getJumpmanPosition()
    r, dist = get_reward(sim, dist,jm)
    reward += r
    print(f"{reward} done = {done} y = {sim.getJumpmanPosition()[1]}, j = {jm.jumping}, f= {jm.fallingAfterJump}")
    i+=1 
    if i >= 2:
        i = 0 

    renderer.run()