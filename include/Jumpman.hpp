#pragma once
#include <string>
#include "Entity.hpp"

class Jumpman: public Entity{
    private:
        bool _keyboard;
        bool _rendering;
    public:
        bool jumping;
        Jumpman():Entity(0,0,100,100),_keyboard(false),_rendering(false),jumping(false){}        
        void move(std::string direction) override;
        void moveOnStairs(bool stairsContact);
        void draw(sf::RenderWindow& window);
        void jump();
        CollisionBox getCollisionBox(std::string box);

};