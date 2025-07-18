#pragma once
#include "Entity.hpp"

class Obstacle: public Entity{
    private:
        float _width, _height; 
    public:
        Obstacle(float x, float y, float width, float height): Entity(x,y),_width(width),_height(height){}
        void draw(sf::RenderWindow& window);


};