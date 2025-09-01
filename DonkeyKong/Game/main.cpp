#include "Renderer.hpp"

using namespace std;

int main(void){
    Jumpman jumpman;
    Simulation simulation(&jumpman,1700,1500);
    simulation.loadMapFromJson(string(PROJECTPATH)+"/map.json");
    Renderer renderer(simulation,1700,1500);

    while (renderer.isOpen())
    {
        simulation.run();
        renderer.run();
    }
    

}