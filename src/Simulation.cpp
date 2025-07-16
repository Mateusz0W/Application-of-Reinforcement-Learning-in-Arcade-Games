#include "Simulation.hpp"

using namespace std;

void Simulation::run(){
    nextStep();
}
void Simulation::nextStep(){
    for (const auto& entity :this->_entities){
        if(Jumpman* jm = dynamic_cast<Jumpman*>(entity.get())){
            jm->move(keyboardControl());
        }
    }
}

string Simulation::keyboardControl(){
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Left))
        return "Left";
    else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Right))
        return "Right";
    else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Up))
        return "Up";
    else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Down))
        return "Down";
    else
        return "";
}
const std::vector<std::unique_ptr<Entity>>& Simulation::getEntities() const {
    return _entities;
}