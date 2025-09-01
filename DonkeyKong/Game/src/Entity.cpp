#include "Entity.hpp"
#include <iostream>

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
void Entity::setTexture(std::string path){
    if(!this->_texture.loadFromFile(path)){
        std::cerr<<"Can't load texture";
        return;
    }
}
bool Entity::isOutsideMap(unsigned int mapX, unsigned int mapY){
    if(0 <= this->_dx && this->_dx <= mapX && 0 <= this->_dy && this->_dy <= mapY)
        return false;
    return true;
}