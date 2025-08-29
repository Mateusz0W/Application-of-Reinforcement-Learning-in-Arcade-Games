#include "Renderer.hpp"

using namespace std;

int main(void){
    Jumpman jumpman;
    Simulation simulation(&jumpman,1500,1700);
    simulation.loadMapFromJson(string(PROJECTPATH)+"/map.json");
    Renderer renderer(simulation,1500,1700);

    //simulation.run();
    renderer.run();
}