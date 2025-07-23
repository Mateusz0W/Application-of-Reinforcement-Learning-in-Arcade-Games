#pragma once
#include "Entity.hpp"

class Obstacle: public Entity{
    private:
    std::string _type;
    public:
        Obstacle(float x, float y, float width, float height,std::string type): Entity(x,y,width,height),_type(type){}
        void draw(sf::RenderWindow& window);
        std::string getType();


};