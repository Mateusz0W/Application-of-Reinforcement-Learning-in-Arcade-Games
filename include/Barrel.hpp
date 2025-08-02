#include "Entity.hpp"

class Barrel : public Entity{
    private:
        float _radius;
        float _prevY;
    public:
        Barrel(float dx, float dy, float radius): Entity(dx,dy), _radius(radius){}
        void draw(sf::RenderWindow& window) override;
        void move(std::string direction) override;
        bool checkCollision(Entity *entity) override;
        std::string chooseMoveDirection();
};