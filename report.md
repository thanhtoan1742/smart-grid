|                   | bfs (undirected) | dijkstra | a*  |
| ----------------- | ---------------- | -------- | --- |
| conventional 1    | 0.0152s          | Na       | Na  |
| conventional 4    | 0.0045s          | Na       | Na  |
| configurational 1 | 0.0002s          | Na       | Na  |
| configurational 4 | 0.0002s          | Na       | Na  |


## Comparing shortest path algorithm



## Improvement in model
- The "trans" transition's guard condition: p_generated > 0 and p_consumer < #c(consumer)
-> This make sure if we've already satisfied a customer, we won't give them any more
power -> less state in state space.

- fun fn_cons(con: NODE, p_generated: POWER, p_consumed: POWER)
	= (con, min(p_consumed + p_generated, #c(con)));
- fun fn_trans( con: NODE, p_generated: POWER, p_consumed: POWER)
	= p_generated - min(p_generated, #c(con) - p_consumed);
-> Do not serve a customer more than what they need.


## Configurational approach drawbacks

Because we simplified the topology, many information simply lost. This makes:
- Assumed the smart grid is strongly connected.
- Harder to figure out the actual configuration of the smart grid to get the disired state.

Model forced to use 100% given power when in reality we can use smaller fraction to reduce cost.
