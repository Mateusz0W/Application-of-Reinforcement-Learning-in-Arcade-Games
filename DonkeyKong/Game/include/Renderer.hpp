#pragma once
#include "Simulation.hpp"
#include <SFML/Graphics.hpp>

class Renderer{
    private:
        Simulation& _simulation;
        unsigned int _windowHeight;
        unsigned int _windowWidth;
        sf::RenderWindow _window;
    public:
        Renderer() = delete;
        Renderer(Simulation &simulation,unsigned int windowWidth,unsigned int windowHeight):_simulation(simulation),_windowHeight(windowHeight),_windowWidth(windowWidth),_window(sf::VideoMode({windowWidth, windowHeight}), "Donkey Kong"){}
        void drawFrame(sf::RenderWindow& window);
        void run();
        bool isOpen() const;  
};
