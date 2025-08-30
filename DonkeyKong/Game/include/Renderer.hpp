#pragma once
#include "Simulation.hpp"
#include <SFML/Graphics.hpp>

class Renderer{
    private:
        Simulation& _simulation;
        unsigned int _windowHeight;
        unsigned int _windowWidth;
    public:
        Renderer() = delete;
        Renderer(Simulation &simulation,unsigned int windowHeight,unsigned int windowWidth):_simulation(simulation),_windowHeight(windowHeight),_windowWidth(windowWidth){}
        void drawFrame(sf::RenderWindow& window);
        void run();
};
