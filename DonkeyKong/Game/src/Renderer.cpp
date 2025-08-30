#include "Renderer.hpp"

void Renderer::drawFrame(sf::RenderWindow& window){
    const auto& entities = _simulation.getEntities();
    int numOfBarrels = _simulation.getBarrelsCounter();
    int entitiesSize = entities.size();

    for(size_t i = entitiesSize - numOfBarrels; i -- > 1;)
        entities[i]->draw(window);

    entities[0]->draw(window);

    for(size_t i = entities.size() - numOfBarrels; i < entitiesSize; i++)
        entities[i]->draw(window);
}
void Renderer::run(){
    sf::RenderWindow window(sf::VideoMode({_windowWidth,_windowHeight}),"Donkey Kong");
    while (window.isOpen()) {
        while (const std::optional event = window.pollEvent())
        {
            if (event->is<sf::Event::Closed>())
                window.close();
        }
        this->_simulation.run();
        window.clear(sf::Color::Black);
        this->drawFrame(window);
        window.display();
    }
}