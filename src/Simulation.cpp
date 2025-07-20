#include "Simulation.hpp"
#include "Obstacle.hpp"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>


using namespace std;
using json = nlohmann::json;

void Simulation::run(){
    nextStep();
}

void Simulation::nextStep(){
    bool groundContact = false;
    bool stairsContact = false;
    Jumpman* jm = dynamic_cast<Jumpman*>(_entities[0].get());
    for (const auto& entity :this->_entities){
        if(jm == entity.get())
            continue;
        groundContact |= this->_entities[0]->checkCollision(entity.get(),jm->getCollisionBox("groundBox"));
        stairsContact |= this->_entities[0]->checkCollision(entity.get(),jm->getCollisionBox("sideBox"));
    }
    jm->move(keyboardControl());
    jm->moveOnStairs(stairsContact);
    this->_entities[0]->gravity(groundContact);
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

void Simulation::loadMapFromJson(string fileName){
    ifstream file(fileName);

    if(!file.is_open()){
        cerr<<"Can't open file ";
        return ;
    }
    json j;
    file >> j;

    for (const auto &obs: j["obstacles"]){
        _entities.push_back(make_unique<Obstacle>(
            obs["x"].get<float>(),
            obs["y"].get<float>(),
            obs["width"].get<float>(),
            obs["height"].get<float>()
        ));
    }

}