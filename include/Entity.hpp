#pragma once
#include <string>
#include <SFML/Graphics.hpp>

class Entity{
    protected:
        float _dx;
        float _dy;
    public:
        Entity(float dx = 0.f, float dy = 0.f) : _dx(dx), _dy(dy) {} 
        virtual void move(std::string direction) =0;
        virtual void draw(sf::RenderWindow& window) =0;
        virtual ~Entity() = default;
};