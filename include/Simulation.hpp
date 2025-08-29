#pragma once
#include "Entity.hpp"
#include <vector>
#include <string>
#include <memory>
#include "Jumpman.hpp"
#include <chrono>

class Simulation{
    private:
        std::vector<std::unique_ptr<Entity>> _entities;
        std::chrono::steady_clock::time_point _lastUpdate;
        int _barrelsCounter;
        bool _reset;
    public:
        unsigned int _windowX, _windowY;
        Simulation() = delete;
        Simulation(Jumpman *jm, unsigned int windowX, unsigned int windowY): _windowX(windowX), _windowY(windowY), _barrelsCounter(0), _reset(false){
            _entities.push_back(std::unique_ptr<Jumpman>(jm));
            _lastUpdate = std::chrono::steady_clock::now();
        }
        void run();
        void nextStep();
        std::string keyboardControl();
        const std::vector<std::unique_ptr<Entity>>& getEntities() const ;
        void loadMapFromJson(std::string fileName);
        void addBarrel();
        void removeBarrels(bool removeAll = false);
        int getBarrelsCounter();
        void restart();
};