#include "Barrel.hpp"
#include <algorithm>
#include <utility>
#include <cmath>

using namespace std;
using Vector2D = pair<float, float>;

void Barrel::draw(sf::RenderWindow& window){
    sf::CircleShape circle(this->_radius);
    circle.setFillColor(sf::Color::Red);
    circle.setPosition(sf::Vector2f(this->_dx,this->_dy));
    window.draw(circle);
}
void Barrel::move(string direction){
    if (direction == "Left")
        this->_dx -= 1.;
    else if (direction == "Right")
        this->_dx += 1.;
    else if (direction == "Down")
        this->_dy +=1.;
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
    static int flag = 0;
    static int currentDirection = 1;
    static string direction = "Right";
    if (this->groundContact){
        direction = (currentDirection == 1) ? "Right" : "Left";
        if (flag){
            if (this->_dy - this->_prevY > 20){
                currentDirection *= -1;
                direction = (currentDirection == 1) ? "Right" : "Left";
            }
            flag = 0;
        }
        this->_prevY = this->_dy;
    }
    else{
        flag = 1;  
        direction = "";
    }
    
    return direction;
}