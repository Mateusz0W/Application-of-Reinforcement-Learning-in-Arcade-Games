#include "Renderer.hpp"

using namespace std;

int main(void){
    vector<unique_ptr<Entity>> entities;
    entities.push_back(make_unique<Jumpman>());
    Simulation simulation(std::move(entities));
    simulation.loadMapFromJson("../map.json");
    Renderer renderer(simulation,1500,1500);

    //simulation.run();
    renderer.run();
}