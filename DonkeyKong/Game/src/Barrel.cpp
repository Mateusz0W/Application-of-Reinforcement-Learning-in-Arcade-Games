#include "Barrel.hpp"
#include <algorithm>
#include <utility>
#include <cmath>
#include <random>

using namespace std;
using Vector2D = pair<float, float>;

void Barrel::draw(sf::RenderWindow& window){
    sf::CircleShape circle(this->_radius);
    circle.setTexture(&_texture);
    circle.setPosition(sf::Vector2f(this->_dx - this->_radius, this->_dy - this->_radius));
    window.draw(circle);
}
void Barrel::move(string direction){
    if (direction == "Left")
        this->_dx -= 1.5;
    else if (direction == "Right")
        this->_dx += 1.5;
    else if (direction == "Down")
        this->_dy += 1.5;
}
bool Barrel::checkCollision(Entity *entity){
    auto clamp = [](float value, float minValue, float maxValue){
        return max(minValue, min(maxValue,value));
    };

    Vector2D vector = {
        this->_dx - (entity->getX() + entity->getWidth() / 2),
        this->_dy - (entity->getY() +entity->getHeight() / 2)
    };
    Vector2D entityHalfExtents = {
        entity->getWidth() / 2,
        entity->getHeight() / 2,
    };

    float clammpedX = clamp(vector.first, -entityHalfExtents.first, entityHalfExtents.first);
    float clammpedY = clamp(vector.second, -entityHalfExtents.second, entityHalfExtents.second);

    Vector2D closestPoint = {
        (entity->getX() + entity->getWidth() / 2) + clammpedX,
        (entity->getY() +entity->getHeight() / 2) + clammpedY
    };
    Vector2D newVector = {
        closestPoint.first - this->_dx,
        closestPoint.second - this->_dy
    };

    float diff = sqrt( pow(newVector.first,2) + pow(newVector.second,2));

    if (diff <= this->_radius)
        return true; //Hit

    return false; //No hit
}
string Barrel::chooseMoveDirection(){

    if(this->_goingDown)
        this->_direction = "Down";
    else if (this->groundContact){
        this->_direction = (this->currentDirection == 1) ? "Right" : "Left";
        if (this->_flag){
            if (this->_dy - this->_prevY > 20){
                this->currentDirection *= -1;
                this->_direction = (this->currentDirection == 1) ? "Right" : "Left";
            }
            this->_flag = 0;
        }
        this->_prevY = this->_dy;
    }
    else{
        this->_flag = 1;  
        this->_direction = "";
    }
    
    return this->_direction;
}
void Barrel::moveOnLadder(Entity *entity){  
    random_device rd; 
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0,1);

    float ladderTop = entity->getY();
    float ladderCenterX = entity->getX() + entity->getWidth() / 2;
    float prevState = this->_goingDown;
   
    if(this->_dy < ladderTop && this->_dx == ladderCenterX && dist(gen))
        this->_goingDown = true;
    if(!this->_prevGroundContact && this->groundContact)
        this->_goingDown = false;
    if(prevState && !this->_goingDown)
        this->currentDirection *= -1;

    this->_prevGroundContact = this->groundContact;
}
void Barrel::resetFlags(){
    this->ladderContact = false;
    this->groundContact = false;
    this->_climbingDown = false;
}