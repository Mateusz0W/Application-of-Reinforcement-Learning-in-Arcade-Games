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
    else if (direction == "Jump" || this->jumping)
        this->jump();
}

void Jumpman::draw(sf::RenderWindow& window){
    sf::RectangleShape rectangle(sf::Vector2f(this->_width,this->_height));
    rectangle.setFillColor(sf::Color::Green);
    rectangle.setPosition(sf::Vector2f(this->_dx,this->_dy));
    window.draw(rectangle); 
}
CollisionBox Jumpman::getCollisionBox(string box){
    if (box == "sideBox"){
        return CollisionBox(
            this->_dx + this->_width,      // xMax
            this->_dx,                     // xMin
            this->_dy + this->_height * 0.9,  // yMax
            this->_dy + this->_height * 0.7 // yMin
        );
    }
    else if (box == "groundBox"){
        return CollisionBox(
            this->_dx + this->_width,      // xMax
            this->_dx,                     // xMin
            this->_dy + this->_height,       // yMax
            this->_dy + this->_height * 0.9 // yMin
        );
    }
    else if (box == "ladderBox"){
        return CollisionBox(
            this->_dx + this->_width - 20,      //xMax
            this->_dx + 20,                     //xMin
            this->_dy + this->_height - 20,     //yMax
            this->_dy + 20                      //yMin
        );
    }
    throw std::invalid_argument("Unknown collision box: " + box);
}
void Jumpman::moveOnStairs(bool stairsContact){
    if (stairsContact)
        this->_dy -= 11;
}
void Jumpman::jump(){
    static int counter = 0;
    if (counter <100){
        this->_dy-=3;
        this->jumping = true;
        counter ++;
    }
    else{
        counter = 0;
        this->jumping = false;
    }
}
