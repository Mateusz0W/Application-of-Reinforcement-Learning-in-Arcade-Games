#pragma once
#include "Entity.hpp"
#include <vector>
#include <string>
#include <memory>
#include "Jumpman.hpp"

class Simulation{
    private:
        std::vector<std::unique_ptr<Entity>> _entities;
    public:
        unsigned int _windowX, _windowY;
        Simulation() = delete;
        Simulation(std::vector<std::unique_ptr<Entity>>&& entities,unsigned int windowX, unsigned int windowY):_entities(std::move(entities)), _windowX(windowX), _windowY(windowY){}
        void run();
        void nextStep();
        std::string keyboardControl();
        const std::vector<std::unique_ptr<Entity>>& getEntities() const ;
        void loadMapFromJson(std::string fileName);
        void addBarrel();
        void removeBarrels();
};