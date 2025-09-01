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
    while (const std::optional event = _window.pollEvent()) {
        if (event->is<sf::Event::Closed>()) {
            _window.close();
            return; 
        }
    }

    _window.clear(sf::Color::Black);
    this->drawFrame(_window);
    _window.display();
}
bool Renderer::isOpen() const {
    return _window.isOpen();
}