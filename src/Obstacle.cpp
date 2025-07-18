#include "Obstacle.hpp"

void Obstacle::draw(sf::RenderWindow& window){
    sf::RectangleShape rectangle(sf::Vector2f(this->_width,this->_height));
    rectangle.setFillColor(sf::Color::White);
    rectangle.setPosition(sf::Vector2f(this->_dx,this->_dy));
    window.draw(rectangle);
}