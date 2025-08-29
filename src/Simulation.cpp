#include "Simulation.hpp"
#include "Obstacle.hpp"
#include "Barrel.hpp"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>
#include <random>


using namespace std;
using json = nlohmann::json;

void Simulation::run(){
    addBarrel();
    nextStep();
    removeBarrels();
    restart();
}

void Simulation::nextStep(){
    Jumpman* jm = dynamic_cast<Jumpman*>(_entities[0].get());
    for (const auto& entity :this->_entities){
        if(jm == entity.get())
            continue;
        else if(Obstacle *obs = dynamic_cast<Obstacle*>(entity.get())){
            if (obs->getType() == "platform"){
                jm->groundContact |= jm->checkCollision(obs,jm->getCollisionBox("groundBox"));
                jm->stairsContact |= jm->checkCollision(obs,jm->getCollisionBox("sideBox"));
            }
            else if (obs->getType() == "ladder"){
                jm->ladderContact |= jm->checkCollision(obs,jm->getCollisionBox("ladderBox"));
            }
        }
        else if(Barrel *brl = dynamic_cast<Barrel*>(entity.get())){
            if(brl->checkCollision(jm)){
                // TODO: implement end game logic
                _reset = true;
            }
            for(int i=1;i<_entities.size();i++){
                if(dynamic_cast<Barrel*>(_entities[i].get()))
                    break;
                else if (Obstacle *obs = dynamic_cast<Obstacle*>(_entities[i].get())){
                    if(obs->getType() == "platform")
                        brl->groundContact |= brl->checkCollision(obs);
                    else if (obs->getType() == "ladder"){
                        if (brl->checkCollision(obs))
                           brl->moveOnLadder(obs);
                    }
                }
            }

            brl->move(brl->chooseMoveDirection());
            brl->gravity();
        }
    }
    string moveDirection = keyboardControl();
    // first condition prevents from double jump. Second condition prevents form stay in the air.
    if ((moveDirection == "Jump" && !jm->groundContact ) || (moveDirection == "Up" && !jm->groundContact && !jm->ladderContact))
        moveDirection = "";
    jm->move(moveDirection);
    jm->moveOnStairs();
    if (moveDirection != "Up" || !jm->ladderContact)
        jm->gravity();

    // TODO: Implement flag reset
    jm->stairsContact = false;
    for(const auto& entity :this->_entities)
        entity.get()->resetFlags();
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

void Simulation::addBarrel(){
    static chrono::seconds timeBetweenBarrels{0};
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(2,6);
    auto currentTime = std::chrono::steady_clock::now();
    if(currentTime - this->_lastUpdate >= timeBetweenBarrels){
        this->_entities.push_back(make_unique<Barrel>(100,245,35));
        timeBetweenBarrels = chrono::seconds(dist(gen));
        this->_lastUpdate = std::chrono::steady_clock::now();
        this->_barrelsCounter++;
    }
}
void Simulation::removeBarrels(bool removeAll){
   for(int idx = this->_entities.size() - 1; idx > 0; idx--){
        if(Barrel *brl = dynamic_cast<Barrel*>(this->_entities[idx].get())){
            if(brl->isOutsideMap(this->_windowX,this->_windowY) || removeAll){
                this->_entities.erase(this->_entities.begin() + idx);
                this->_barrelsCounter--;
            }
        }
        else
            break;
   }
}
int Simulation::getBarrelsCounter(){
    return _barrelsCounter;
}
void Simulation::restart(){
    if(_reset){
        removeBarrels(true);
        auto *jm = dynamic_cast<Jumpman*>(_entities[0].get());
        jm->restart();
        _reset = false;
    }
}