#include "Obstacle.hpp"

using namespace std;

void Obstacle::draw(sf::RenderWindow& window){
    sf::RectangleShape rectangle(sf::Vector2f(this->_width,this->_height));
    if (this->_type == "platform")
        rectangle.setFillColor(sf::Color::White);
    else 
        rectangle.setFillColor(sf::Color::Blue);
    rectangle.setPosition(sf::Vector2f(this->_dx,this->_dy));
    window.draw(rectangle);
}
string Obstacle::getType(){
    return this->_type;
}