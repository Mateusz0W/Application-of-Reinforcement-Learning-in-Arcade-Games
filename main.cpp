#include "Renderer.hpp"

using namespace std;

int main(void){
    vector<unique_ptr<Entity>> entities;
    entities.push_back(make_unique<Jumpman>());
    Simulation simulation(std::move(entities),1500,1700);
    simulation.loadMapFromJson("../map.json");
    Renderer renderer(simulation,1500,1700);

    //simulation.run();
    renderer.run();
}