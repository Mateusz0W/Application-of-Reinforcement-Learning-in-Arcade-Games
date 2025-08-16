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
        sf::Texture _texture;
    public:
        bool groundContact;
        bool ladderContact;
        Entity(float dx, float dy): _dx(dx), _dy(dy){}
        Entity(float dx, float dy, float width, float height) : _dx(dx), _dy(dy), _width(width), _height(height), groundContact(false), ladderContact(false){} 
        virtual void move(std::string direction){}
        virtual void draw(sf::RenderWindow& window) =0;
        virtual bool checkCollision(Entity *entity,CollisionBox box);
        virtual bool checkCollision(Entity *entity){return false;};
        virtual void gravity();
        virtual void resetFlags();
        void setTexture(std::string path); 
        float getX();
        float getY();
        float getWidth();
        float getHeight();
        virtual ~Entity() = default;
};