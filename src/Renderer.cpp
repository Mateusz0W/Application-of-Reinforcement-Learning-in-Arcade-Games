#include "Renderer.hpp"

void Renderer::drawFrame(sf::RenderWindow& window){
    for(const auto& entity : this->_simulation.getEntities())
        entity->draw(window);
}
void Renderer::run(){
    sf::RenderWindow window(sf::VideoMode({_windowWidth,_windowHeight}),"Donkey Kong");
    while (window.isOpen()) {
        while (const std::optional event = window.pollEvent())
        {
            // "close requested" event: we close the window
            if (event->is<sf::Event::Closed>())
                window.close();
        }
        this->_simulation.run();
        window.clear(sf::Color::Black);
        this->drawFrame(window);
        window.display();
    }
}