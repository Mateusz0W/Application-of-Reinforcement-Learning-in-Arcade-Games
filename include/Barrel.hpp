#include "Entity.hpp"

class Barrel : public Entity{
    private:
        float _radius;
        float _prevY;
        bool _climbingDown;
        bool _goingDown;
        bool _prevGroundContact;
    public:
        int currentDirection;
        Barrel(float dx, float dy, float radius): Entity(dx,dy), _radius(radius), currentDirection(-1),_goingDown(false),_prevGroundContact(true){}
        void draw(sf::RenderWindow& window) override;
        void move(std::string direction) override;
        bool checkCollision(Entity *entity) override;
        std::string chooseMoveDirection();
        void moveOnLadder(Entity *entity);
        void resetFlags() override;
};