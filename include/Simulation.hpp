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
        Simulation() = delete;
        Simulation(std::vector<std::unique_ptr<Entity>>&& entities):_entities(std::move(entities)){}
        void run();
        void nextStep();
        std::string keyboardControl();
        const std::vector<std::unique_ptr<Entity>>& getEntities() const ;
        void loadMapFromJson(std::string fileName);
        void addBarrel();
};