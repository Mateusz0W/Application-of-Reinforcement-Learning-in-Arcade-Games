#include "Simulation.hpp"
#include "Obstacle.hpp"
#include "Barrel.hpp"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>
#include <random>
#include <cmath>
#include <algorithm>

using namespace std;
using json = nlohmann::json;

int Simulation::run(){
    _reset = false;
    _win = false;
    addBarrel();
    nextStep();
    removeBarrels();
    if (_playerMode)
        restart();
    _barrelsPositions.clear();

    return _win | _reset;
}

void Simulation::nextStep(){
    Jumpman* jm = dynamic_cast<Jumpman*>(_entities[0].get());
    _jumpmanPosition = make_tuple(jm->getX(),jm->getY());
    for (const auto& entity :this->_entities){
        if(jm == entity.get())
            continue;
        else if(Obstacle *obs = dynamic_cast<Obstacle*>(entity.get())){
            if (obs->getType() == "platform"){
                if (jm->isJumping())
                    continue;
                jm->groundContact |= jm->checkCollision(obs,jm->getCollisionBox("groundBox"));
                jm->stairsContact |= jm->checkCollision(obs,jm->getCollisionBox("sideBox"));
                if(jm->groundContact) jm->fallingAfterJump = false;
            }
            else if (obs->getType() == "ladder"){
                jm->ladderContact |= jm->checkCollision(obs,jm->getCollisionBox("ladderBox"));
            }
        }
        else if(Barrel *brl = dynamic_cast<Barrel*>(entity.get())){
            if(brl->checkCollision(jm)){
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
            _barrelsPositions.push_back(make_tuple(brl->getX(),brl->getY()));
        }
    }
    //string moveDirection = action;
    string moveDirection = _playerMode ? keyboardControl() : this->action;
    // first condition prevents from double jump. Second condition prevents form stay in the air.
    if ((moveDirection == "Jump" && !jm->groundContact ) || (moveDirection == "Up" && !jm->groundContact && !jm->ladderContact) || moveDirection == "Up" && !jm->ladderContact)
        moveDirection = "";
    jm->move(moveDirection);
    jm->moveOnStairs();
    if (moveDirection != "Up" || !jm->ladderContact)
        jm->gravity();

    // TODO: Implement flag reset
    if(jm->isOutsideMap(this->_windowX,this->_windowY))
        _reset = true;
    if(jm->reachPrincess())
        _win = true;
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
        this->_entities.push_back(make_unique<Barrel>(100.f,245.f,32.f));
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
    if(_reset || _win){
        removeBarrels(true);
        auto *jm = dynamic_cast<Jumpman*>(_entities[0].get());
        jm->restart();
    }
}
vector<tuple<float,float>> Simulation::getBarrelsPositions(){
    // returns 5 closest barrels to jumpman

    Jumpman* jm = dynamic_cast<Jumpman*>(_entities[0].get());
    float jmX = jm->getX();
    float jmY = jm->getY();

    auto distanceToJumpman = [jmX, jmY](const float x, const float y){ 
        return pow(jmX - x,2) + pow(jmY - y, 2);
    };

    sort(_barrelsPositions.begin(),_barrelsPositions.end(),
    [distanceToJumpman](const tuple<float,float> &a, const tuple<float,float> &b){
        auto dist1 = distanceToJumpman(get<0>(a),get<1>(a));
        auto dist2 = distanceToJumpman(get<0>(b),get<1>(b));
        return dist1 < dist2;
    });

    vector<tuple<float,float>> closest;
    int size = _barrelsPositions.size();
    float inf = INFINITY;

    if(size < 5){
        closest.assign(_barrelsPositions.begin(),_barrelsPositions.begin() + size);
        closest.resize(5, make_tuple(inf, inf));
    }
    else
        closest.assign(_barrelsPositions.begin(),_barrelsPositions.begin() + 5);

    return closest;
    
}
tuple<float,float> Simulation::getJumpmanPosition(){
    return _jumpmanPosition;
}