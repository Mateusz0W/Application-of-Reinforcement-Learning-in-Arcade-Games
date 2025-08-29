#pragma once
#include <string>
#include "Entity.hpp"

class Jumpman: public Entity{
    public:
        bool jumping;
        bool stairsContact;
        Jumpman():Entity(0,0,50,100),jumping(false),stairsContact(false){
            this->setTexture(std::string(PROJECTPATH)+"/assets/Jumpman.png");
        }        
        void move(std::string direction) override;
        void moveOnStairs();
        void draw(sf::RenderWindow& window);
        void jump();
        CollisionBox getCollisionBox(std::string box);
        void restart();
};