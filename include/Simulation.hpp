#pragma once
#include "Jumpman.hpp"
#include "Entity.hpp"
#include <vector>
#include <string>
#include <memory>

class Simulation{
    private:
        std::vector<std::unique_ptr<Entity>> _entities;
    public:
        Simulation() = delete;
        Simulation(std::vector<std::unique_ptr<Entity>>&& entities):_entities(std::move(entities)){}
        void run();
        void nextStep();
        std::string keyboardControl();
        const std::vector<std::unique_ptr<Entity>>& getEntities() const ;
};