#pragma once
#include <string>
#include "Entity.hpp"

class Jumpman: public Entity{
    private:
        bool _keyboard;
        bool _rendering;
    public:
        bool jumping;
        bool stairsContact;
        Jumpman():Entity(0,0,50,100),_keyboard(false),_rendering(false),jumping(false),stairsContact(false){
            this->setTexture("../assets/Jumpman.png");
        }        
        void move(std::string direction) override;
        void moveOnStairs();
        void draw(sf::RenderWindow& window);
        void jump();
        CollisionBox getCollisionBox(std::string box);

};