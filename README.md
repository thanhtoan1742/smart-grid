# Smart grid configuration searcher

Configuration searching algorithms and experiments for configurational approach modelled
smart grid.

## Modelling

The original grid is modelled as an undirected graph. The type of node defines the node's
behavior. We have the followings types and their parameters:
- Generator: generate power.
    - Capacity: amount of maximum power can be generated in a unit of time.
    - Generating Amount: amount of currently generating power.
    - Cost (optional): the cost to generate 1 unit of power in a unit of time.
- Consumer: consume power.
    - Capacity: amount of power needed in a unit of time.
    - Consuming Amount: amount of currently consuming power.
- Bus: power junction.
- Circuit breaker: control whether the power can flow through this node.
    - Status: on/off.


## Problem
Given the topology, properties and a state of a grid, configure the grid so that
it satisfies criteria and optimizes a certain criterion.

Topology of the grid:
- How the grid is connected.

Property of the grid:
- Generators' capacity.
- Generators' cost.

State of grid:
- Consumers' capacity.
- Some circuit breaker state are set (can not be changed).

What can be configured:
- The generating amount of generators
_ The circuit breaker states

Criteria need to be satisfied:
- For each consumer, its consuming amount >= its capacity.

Criteria need to be optimized:
- The cost to switch from current state to the desired state.
- Smallest number of curcuit breaker need to be changed.
