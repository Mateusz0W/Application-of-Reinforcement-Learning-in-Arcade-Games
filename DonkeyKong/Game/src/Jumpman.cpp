#include "Jumpman.hpp"

using namespace std;

void Jumpman::move(string direction){
    if (direction == "Left")
        this->_dx -= 1.;
    if (direction == "Right")
        this->_dx += 1.;
    if (direction == "Up")
        this->_dy -= 1.;
    if (direction == "Down")
        this->_dy +=1.;
    if (direction == "Jump" || this->jumping)
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
    bool prevJumpingState = this->jumping;
    this->jumping = true;

    if(!prevJumpingState && this->jumping)
        this->jumpStartY = this->_dy;

    this->_dy += jumpStrength;
    jumpStrength += 0.1f;
    if (jumpStrength > 0){
        this->jumping = false;
        this->fallingAfterJump = true;
        jumpStrength = -5.f;
    }
}
void Jumpman::restart(){
    this->resetFlags();
    this->stairsContact = false;
    this->jumping = false;
    this->_dx = 50;
    this->_dy = 1315;
    this->fallingAfterJump = false;
}
void Jumpman::gravity(){
    if (!groundContact){
        _Vy += 0.01;
        if (_Vy >= 1.5) _Vy = 1.5;
        this->_dy += _Vy;
    }
    else
        _Vy = 0;
}

bool Jumpman::reachPrincess(){
    if(_dy <= 70)
        return true;
    else
        return false;
}

bool Jumpman::isJumping(){
    if (jumpStartY - _dy < 5 && (fallingAfterJump || jumping))
        return false;
    else if (fallingAfterJump || jumping)
        return true;

    return false;
}
