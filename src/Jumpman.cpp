#include "Jumpman.hpp"

using namespace std;

void Jumpman::move(string direction){
    if (direction == "Left")
        this->_dx -= 1.;
    else if (direction == "Right")
        this->_dx += 1.;
    else if (direction == "Up")
        this->_dy -= 1.;
    else if (direction == "Down")
        this->_dy +=1.;
}

void Jumpman::draw(sf::RenderWindow& window){
    sf::RectangleShape rectangle(sf::Vector2f(100.f,100.f));
    rectangle.setFillColor(sf::Color::Green);
    rectangle.setPosition(sf::Vector2f(this->_dx,this->_dy));
    window.draw(rectangle);
}