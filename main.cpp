#include "Renderer.hpp"

using namespace std;

int main(void){
    vector<unique_ptr<Entity>> entities;
    entities.push_back(make_unique<Jumpman>());
    Simulation simulation(std::move(entities));
    Renderer renderer(simulation,1500,1200);

    //simulation.run();
    renderer.run();
}