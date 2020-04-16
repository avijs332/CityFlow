#include "engine/engine.h"
#include "engine/archive.h"

#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

namespace py = pybind11;
using namespace py::literals;

PYBIND11_MODULE(rtc, m) {
    py::class_<RTC::Engine>(m, "Engine")
        .def(py::init<const std::string&, int>(),
            "config_file"_a,
            "thread_num"_a=1
        )
        .def("next_step", &RTC::Engine::nextStep)
        .def("get_vehicle_count", &RTC::Engine::getVehicleCount)
        .def("get_vehicles", &RTC::Engine::getVehicles, "include_waiting"_a=false)
        .def("get_lane_vehicle_count", &RTC::Engine::getLaneVehicleCount)
        .def("get_lane_waiting_vehicle_count", &RTC::Engine::getLaneWaitingVehicleCount)
        .def("get_lane_vehicles", &RTC::Engine::getLaneVehicles)
        .def("get_vehicle_speed", &RTC::Engine::getVehicleSpeed)
        .def("get_vehicle_location", &RTC::Engine::getVehicleLocation)
        .def("get_vehicle_corners", &RTC::Engine::getVehicleCorners)
        .def("get_vehicle_distance", &RTC::Engine::getVehicleDistance)
        .def("get_leader", &RTC::Engine::getLeader, "vehicle_id"_a)
        .def("get_current_time", &RTC::Engine::getCurrentTime)
        .def("get_average_travel_time", &RTC::Engine::getAverageTravelTime)
        .def("set_tl_phase", &RTC::Engine::setTrafficLightPhase, "intersection_id"_a, "phase_id"_a)
        .def("set_vehicle_speed", &RTC::Engine::setVehicleSpeed, "vehicle_id"_a, "speed"_a)
        .def("set_replay_file", &RTC::Engine::setReplayLogFile, "replay_file"_a)
        .def("set_random_seed", &RTC::Engine::setRandomSeed, "seed"_a)
        .def("set_save_replay", &RTC::Engine::setSaveReplay, "open"_a)
        .def("push_vehicle", (void (RTC::Engine::*)(const std::map<std::string, double>&, const std::vector<std::string>&)) &RTC::Engine::pushVehicle)
        .def("reset", &RTC::Engine::reset, "seed"_a=false)
        .def("load", &RTC::Engine::load, "archive"_a)
        .def("snapshot", &RTC::Engine::snapshot)
        .def("load_from_file", &RTC::Engine::loadFromFile, "path"_a);

    py::class_<RTC::Archive>(m, "Archive")
        .def(py::init<const RTC::Engine&>())
        .def("dump", &RTC::Archive::dump, "path"_a);
#ifdef VERSION
    m.attr("__version__") = VERSION;
#else
    m.attr("__version__") = "dev";
#endif
}