#include "Entity.hpp"

class Barrel : public Entity{
    private:
        float _radius;
        float _prevY;
        bool _climbingDown;
        bool _goingDown;
        bool _prevGroundContact;
        std::string _direction;
        bool _flag;
    public:
        int currentDirection;
        Barrel(float dx, float dy, float radius): Entity(dx,dy), _radius(radius), currentDirection(1),_goingDown(false),_prevGroundContact(true),_direction("Right"),_flag(false){
            this->setTexture("../assets/Barrel.png");
        }
        void draw(sf::RenderWindow& window) override;
        void move(std::string direction) override;
        bool checkCollision(Entity *entity) override;
        std::string chooseMoveDirection();
        void moveOnLadder(Entity *entity);
        bool isOutsideMap(unsigned int mapX, unsigned int mapY);
        void resetFlags() override;
};