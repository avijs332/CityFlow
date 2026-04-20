# RTC — Road Traffic Control

RTC is a multi-agent reinforcement learning environment for large-scale city traffic scenario.

Our aim is to eliminate the need for traditional traffic lights by intelligently controlling the speed at which vehicles approach and enter intersections. Under the assumption that autonomous vehicles can receive and execute external control instructions, RTC coordinates multiple agents in real time to enable safe, efficient, and continuous intersection crossing without relying on stop-and-go signaling.

Instead of managing traffic through discrete light phases, RTC treats each vehicle as an adaptive agent within a shared urban system. By adjusting vehicle speeds before they reach conflict zones, the system seeks to reduce congestion, improve traffic flow, minimize unnecessary stopping, and increase the overall throughput of road networks.

## Overview

RTC models traffic control as a multi-agent reinforcement learning problem in which vehicles, intersections, or infrastructure controllers can act as agents depending on the environment design. The system is intended for large-scale urban scenarios, where many interacting participants must be coordinated under dynamic and uncertain conditions.

The core idea is simple: rather than forcing vehicles to stop at intersections and wait for permission to proceed, RTC computes how and when each vehicle should approach an intersection so that crossings remain conflict-free and efficient. In this framework, motion planning and traffic control become part of the same coordinated decision-making process.

## Objectives

RTC is designed around several primary goals:

- Eliminate or drastically reduce dependence on traffic lights
- Maintain safe, collision-free movement through intersections
- Improve traffic throughput across dense urban networks
- Reduce delays, idle time, and stop-and-go behavior
- Lower energy waste and emissions caused by unnecessary braking and acceleration
- Enable scalable coordination across many vehicles and intersections

## Key Idea

Traditional traffic systems rely on binary logic: stop or go. RTC replaces this with continuous control. Vehicles do not simply wait for a green signal; instead, they are assigned speed profiles that regulate when they arrive at and pass through intersections.

This allows the system to:

- Sequence vehicles more efficiently
- Smooth traffic flow across connected roads
- Resolve intersection conflicts without full stops where possible
- Adapt in real time to changing traffic conditions

In an autonomous-vehicle setting, this makes it possible to transform intersections from signalized waiting points into coordinated flow-management zones.

## Why Reinforcement Learning?

Urban traffic is a highly dynamic, multi-agent problem with complex interactions, delayed rewards, and competing objectives such as safety, speed, and fairness. Reinforcement learning provides a natural framework for learning control policies that can adapt to these conditions.

A multi-agent setup is especially important because:

- Many vehicles influence one another simultaneously
- Local decisions at one intersection affect downstream traffic
- Coordination must emerge across a distributed system
- Policies must remain robust under varying traffic densities and patterns

RTC therefore serves both as a research environment and as a foundation for experimenting with decentralized and centralized traffic coordination strategies.

## Environment Scope

RTC is intended to support:

- Large-scale city road networks
- Multiple intersections operating simultaneously
- Vehicle-level or controller-level agent definitions
- Continuous or discrete action spaces
- Reward structures combining safety, efficiency, smoothness, and fairness
- Simulation of dense, realistic traffic scenarios

## Research Vision

The long-term vision of RTC is to explore whether intelligent coordination can outperform traditional traffic signal systems in future autonomous mobility networks. Rather than asking when a light should turn green, RTC asks a more fundamental question:

**Can intersections function safely and efficiently without traffic lights at all, if vehicles are coordinated intelligently enough before entering them?**

RTC is built to investigate that question at scale.

## Potential Metrics

Example evaluation metrics include:

- Collision rate
- Average vehicle delay
- Intersection throughput
- Average travel time
- Number of full stops per vehicle
- Speed variance and ride smoothness
- Queue length
- Network-wide congestion levels

## Future Directions

Possible extensions for RTC include:

- Mixed autonomy scenarios with both autonomous and human-driven vehicles
- Communication constraints and partial observability
- Priority handling for emergency and public transport vehicles
- Coordination across corridors or entire districts
- Sim-to-real transfer for real-world deployment research

## Disclaimer

RTC is a research environment and conceptual framework. Real-world deployment of such a system would require extremely high standards of safety validation, fail-safe mechanisms, regulatory approval, and reliable vehicle-to-infrastructure communication.
----------

.. figure:: https://user-images.githubusercontent.com/44251346/62375390-c9e98600-b570-11e9-8808-e13dbe776f1e.gif
    :align: center
    :alt: demo

