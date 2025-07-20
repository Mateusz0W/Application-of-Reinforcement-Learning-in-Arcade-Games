#pragma once
#include "Entity.hpp"

class Obstacle: public Entity{
    public:
        Obstacle(float x, float y, float width, float height): Entity(x,y,width,height){}
        void draw(sf::RenderWindow& window);


};