#include "Obstacle.hpp"

using namespace std;

void Obstacle::draw(sf::RenderWindow& window){
    sf::RectangleShape rectangle(sf::Vector2f(this->_width,this->_height));
    rectangle.setTexture(&_texture);
    rectangle.setPosition(sf::Vector2f(this->_dx,this->_dy));
    if(_type == "platform")
        rectangle.setTextureRect(sf::IntRect(sf::Vector2i(0,0),sf::Vector2i(_width,_texture.getSize().y)));
    else
        rectangle.setTextureRect(sf::IntRect(sf::Vector2i(0,0),sf::Vector2i(_texture.getSize().x,_height)));
    window.draw(rectangle);
}
string Obstacle::getType(){
    return this->_type;
}