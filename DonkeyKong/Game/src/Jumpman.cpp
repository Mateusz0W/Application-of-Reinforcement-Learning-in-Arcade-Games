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
    rectangle.setTexture(&_texture);
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
    throw invalid_argument("Unknown collision box: " + box);
}
void Jumpman::moveOnStairs(){
    if (stairsContact && !ladderContact) 
        this->_dy -= 11;
}
void Jumpman::jump(){
    static int counter = 0;
    static float Vy = 1.5;
    if (counter <100){
        Vy -= 0.1;
        if (Vy < 0) Vy = 0;
        this->_dy-=2.1 -Vy;
        this->jumping = true;
        counter ++;
    }
    else{
        counter = 0;
        Vy = 1.5;
        this->jumping = false;
    }
}
void Jumpman::restart(){
    this->resetFlags();
    this->stairsContact = false;
    this->jumping = false;
    this->_dx = 0;
    this->_dy = 0;
}
void Jumpman::gravity(){
        if (!groundContact){
        _Vy += 0.05;
        if (_Vy >= 1) _Vy = 1;
        this->_dy += _Vy;
    }
    else
        _Vy = 0;
}
