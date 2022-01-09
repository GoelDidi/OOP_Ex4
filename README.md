# The Pokemon game

![download](https://user-images.githubusercontent.com/88629415/148658851-6ce21efa-9b6d-4032-bea4-9aef4052ca55.jpg)

 ``` 
 The algorithm idea: we calculate the distance, 
 the time it takes to get to the Pokémon by dividing the distance by speed of the agent,
 the sum of the weight of each edge between a certain Pokémon and all of the agents,
 we sum it all together and deduct that sum from the value of the Pokémon,
 the agent that has the maximum value for this equation well go after that Pokémon.
```




## Creators

 - [Goel Didi](https://github.com/GoelDidi)
 - [Michael Agarkov](https://github.com/Michael-Aga)




#  Server: 
## Button:
- #### draw: Call this method to draw the button on the screen.
- #### is_over(self, pos): Pos is the mouse position or a tuple of (x,y) coordinates.
## Client:
- #### start_connection: use with ip='127.0.0.1' , port=6666 to start a new connection to the game server.
- #### __send_message: send the message.
- #### get_agents: returns - json str of agents.
- #### add_agent:  param json_of_node should be in this format: '{"id":0}' (replace 0 with the desired starting node for the agent.) returns 'true' (as str) iff the agent has been added succesfuly
- #### get_graph: returns the graph as json str.
- #### get_info:  returns the current game info.
- #### get_pokemons: returns the current pokemons state as json str.
- #### is_running: returns 'true' (as str) if the game is still running, else: returns 'false' (also str).
- #### time_to_end: returns time to end in mili-seconds str.
- #### start: use start to run the game.
- #### stop: use stop to end the game and upload results.
- #### move: activate all valid choose_next_edge calls.
- #### choose_next_edge: choosing the next destination for a specific agent.
- #### log_in: enter your id as str to login and upload your score to the web server.
- #### stop_connection: use it to close the connection.

## student_code:
- #### scale: get the scaled data with proportions min_data, max_data relative to min and max screen dimensions.
- #### my_scale: decorate scale with the correct values.
- #### calculate_pokemons_location: Calculates the location of the pokemon.
- #### calculate_juiciness: This function returns the value of the pokemon, basically its a part of the algo that the max value is the most worthy pokemon that this agent should get we get the value by calculating the distance/speed so we could know the time it takes to get to the pokemon and then we add the weight of the edges to get to him sum it up in the total_time and then deduct it from the value of the pokemon.
- #### get_pokemon_src_and_dest_from_points: The pokemons that we get from the server don't have a src and dest, so we will do it between 2 nodes.
- #### is_pokemon_on_the_edge_of_2_points: checks if the pokemon is between two nodes, we do that by checking if the pos of the pokemon is on the Straight Equation between 2 nodes.
- #### move_agent: decide the next node that the agent will go to.
- #### add_agent: adds the agents from the server.
- #### pokemon_is_being_caught: checks if the pokemon has an agent assigned that is coming to catch him.
#  Classes: 
## NodeData:
- Node class **:** It holds the values of the Node and Edges from this node to other nodes or other nodes to this node, and key for unique ID and his location.


## DiGraph
###### the class import GraphInterface that represents an interface of a graph.

- #### v_size: Returns the number of vertices in this graph.
- #### e_size: Returns the number of edges in this graph.
- #### get_all_v: return a dictionary of all the nodes in the Graph, each node is represented using a pair (node_id, node_data)
- #### all_in_edges_of_node: return a dictionary of all the nodes connected to (into) node_id , each node is represented using a pair (other_node_id, weight)
- #### all_out_edges_of_node: return a dictionary of all the nodes connected from node_id , each node is represented using a pair (other_node_id, weight)
- #### get_mc: The current version of this graph.
- #### add_edge: Adds an new edge to the graph.
- #### add_node: Adds a new node to the graph.
- #### remove_node: Remove a specific node from the graph.
- #### remove_edge: Remove an specific edge from the graph.

## GraphAlgo
 #### This is the graphClass that all the algorithms would operate in.

We create a graph from the previous class, and on that we will run the algorithm.
- #### get_graph: returns the graph that we preforms the algorithms on.
- #### load_from_json: Loads a graph from a json string.
- #### load_from_json_file: Loads a graph from a json file.
- #### save_to_json: Saves the graph in JSON format to a file.
- #### shortest_path: finds the shortest path between two nodes that the function receive and returns the distance and a list of the path itself.
- #### TSP: Finds the shortest path that visits all the nodes in the list of our Graph.
- #### centerPoint: Finds the node that has the shortest distance to it's farthest node.
- #### plot_graph: Plots the graph. If the nodes have a position the nodes will be placed there.
  #### Otherwise, they will be placed in a random spot.

## matplotlib
- #### This is a class that receives a graph after the creation of nodes and the edges and the class creates a graphical interface on the screen:
- #### plot_graph - we using this in GraphAlgo class and the function takes the lists of the graph that include the position of the nodes and the eges that connect the nodes and draw it on our screen like that (A3): ![A3](https://user-images.githubusercontent.com/88629415/147497833-c82c2205-0c25-449e-a7ae-293233eeab8d.png)

# UML

![Ex4_uml](https://user-images.githubusercontent.com/88629415/148675696-e866ae01-6895-4b81-9ac4-d815d84655fe.png)


## Run Locally

Clone the project

```bash
  git clone https://github.com/Michael-Aga/OOP_Ex4.git
```

open the project directory from where you clone the project

Start the server from the terminal

```bash
  java -jar Ex4_Server_v0.0.jar "your case 0-15"
```
Run the code student_code 

### Or you can watch a 3-minute tutorial video
```bash
  https://www.youtube.com/watch?v=eqQWVtLuEaA
```

