#include "Entity.hpp"

bool Entity::checkCollision(Entity *entity,CollisionBox box){
    return (
        box.xMax > entity->getX() &&
        box.xMin < entity->getX() + entity->getWidth() &&
        box.yMax > entity->getY() &&
        box.yMin < entity->getY() + entity->getHeight()
    );
}
void Entity::gravity(){
    if (!groundContact)
        this->_dy++;
}
float Entity::getX(){
    return _dx;
}
float Entity::getY(){
    return _dy;
}
float Entity::getWidth(){
    return _width;
}
float Entity::getHeight(){
    return _height;
}
void Entity::resetFlags(){
    this->ladderContact=false;
    this->groundContact=false;
}