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
    bool ladderContact = false;
    Jumpman* jm = dynamic_cast<Jumpman*>(_entities[0].get());
    for (const auto& entity :this->_entities){
        if(jm == entity.get())
            continue;
        else if(Obstacle *obs = dynamic_cast<Obstacle*>(entity.get())){
            if (obs->getType() == "platform"){
                groundContact |= jm->checkCollision(obs,jm->getCollisionBox("groundBox"));
                stairsContact |= jm->checkCollision(obs,jm->getCollisionBox("sideBox"));
            }
            else if (obs->getType() == "ladder"){
                ladderContact |= jm->checkCollision(obs,jm->getCollisionBox("ladderBox"));
            }
        }
        
    }
    string moveDirection = keyboardControl();
    if (moveDirection == "Jump" && !groundContact)
        moveDirection = "";
    jm->move(moveDirection);
    jm->moveOnStairs(stairsContact);
    if (moveDirection != "Up" || !ladderContact)
        jm->gravity(groundContact);
}

string Simulation::keyboardControl(){
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Left))
        return "Left";
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Right))
        return "Right";
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Up))
        return "Up";
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Down))
        return "Down";
    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Space))
        return "Jump";
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
            obs["height"].get<float>(),
            obs["type"].get<string>()
        ));
    }

}