#pragma once
#include <string>
#include "Entity.hpp"

class Jumpman: public Entity{
    public:
        bool jumping;
        bool fallingAfterJump;
        bool stairsContact;
        float jumpStrength;
        float jumpStartY;
        Jumpman():Entity(50,1315,60,85),jumping(false), fallingAfterJump(false), stairsContact(false), jumpStrength(-5.f){
            this->setTexture(std::string(PROJECTPATH)+"/assets/Jumpman.png");
        }        
        void move(std::string direction) override;
        void moveOnStairs();
        void draw(sf::RenderWindow& window);
        void jump();
        void gravity() override;
        CollisionBox getCollisionBox(std::string box);
        void restart();
        bool reachPrincess();
        bool isJumping();
};