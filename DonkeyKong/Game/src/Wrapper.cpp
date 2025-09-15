#include<pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Renderer.hpp"
#include "Simulation.hpp"
#include "Entity.hpp"
#include "Jumpman.hpp"

namespace py = pybind11;

PYBIND11_MODULE(DonkeyKongPy, m){
    py::class_<Renderer>(m, "Renderer")
        .def(py::init<Simulation&, unsigned int, unsigned int>())
        .def("run", &Renderer::run)
        .def("isOpen", &Renderer::isOpen);
    
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<Jumpman*, unsigned int, unsigned int, bool>())
        .def("loadMapFromJson", &Simulation::loadMapFromJson)
        .def("getBarrelsPositions", &Simulation::getBarrelsPositions)
        .def("getJumpmanPosition", &Simulation::getJumpmanPosition)
        .def("getReset", &Simulation::getReset)
        .def("getWin", &Simulation::getWin)
        .def("run", &Simulation::run)
        .def("restart", &Simulation::restart)
        .def_readwrite("action", &Simulation::action);

    py::class_<Jumpman>(m, "Jumpman")
        .def(py::init<>())
        .def_readwrite("jumping", &Jumpman::jumping)
        .def_readwrite("ladderContact", &Jumpman::ladderContact)
        .def_readwrite("fallingAfterJump", &Jumpman::fallingAfterJump);
}
