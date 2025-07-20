#pragma once
#include <string>
#include <SFML/Graphics.hpp>

struct CollisionBox{
    float xMin, xMax;
    float yMin, yMax;
    CollisionBox(float xMax,float xMin, float yMax, float yMin): xMax(xMax), xMin(xMin), yMax(yMax), yMin(yMin){}
};

class Entity{
    protected:
        float _dx, _dy;
        float _width, _height; 
    public:
        Entity(float dx = 0.f, float dy = 0.f, float width = 10.f, float height = 10.f ) : _dx(dx), _dy(dy), _width(width), _height(height){} 
        virtual void move(std::string direction){}
        virtual void draw(sf::RenderWindow& window) =0;
        virtual bool checkCollision(Entity *entity,CollisionBox box);
        virtual void gravity(bool groundContact);
        float getX();
        float getY();
        float getWidth();
        float getHeight();
        virtual ~Entity() = default;
};