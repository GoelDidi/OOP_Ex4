import json
from time import sleep
from types import SimpleNamespace

import button
import pygame
from numpy import ones, vstack
from numpy.linalg import lstsq
from numpy.testing import assert_almost_equal
from pygame import *
from pygame import gfxdraw

from server.Button import Button
from server.client import Client

from src.Agent import Agent
from src.GraphAlgo import GraphAlgo
import time
from src.Pokemon import Pokemon

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

# init pygame
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
radius = 15

client = Client()
client.start_connection(HOST, PORT)
graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
info_font = pygame.font.SysFont('Arial', 15, bold=True)

# load the json string into SimpleNamespace Object
graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda node: node.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda node: node.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda node: node.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda node: node.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, my_x_scale=False, my_y_scale=False):
    """ decorate scale with the correct values """
    if my_x_scale:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if my_y_scale:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


# create a button for the stop function
exit_button = Button((255, 0, 0), 0, 0, 50, 50, 'Stop')

# -------------------------------------------- Start of the algo -------------------------------------------------------

# load up the graph
myGraphAlgo = GraphAlgo()
myGraphAlgo.load_from_json(client.get_graph())
myGraph = myGraphAlgo.get_graph()


def calculate_pokemons_location(selected_pokemon):
    """Calculates the location of the pokemon"""
    for node_id, node_data in myGraph.get_all_v().items():
        for connected_id, _ in myGraph.all_out_edges_of_node(node_id).items():
            connected_node_data = myGraph.get_all_v()[connected_id]
            if is_pokemon_on_the_edge_of_2_points(selected_pokemon, [node_data.pos, connected_node_data.pos]):
                return node_data, connected_node_data


def calculate_juiciness(agent, selected_pokemon):
    """
    This function returns the value of the pokemon, basically its a part of the algo that the max value is the most
    worthy pokemon that this agent should get we get the value by calculating the distance/speed so we could know
    the time it takes to get to the pokemon and then we add the weight of the edges to get to him sum it up
    in the total_time and then deduct it from the value of the pokemon
    """
    agent_node = agent.src
    pokemon_source_node = selected_pokemon.src
    distance, _ = myGraphAlgo.shortest_path(agent_node, pokemon_source_node)
    time_to_reach_pokemon_source = distance / agent.speed
    time_to_run_over_the_pokemons_edge = myGraph.get_all_v()[pokemon_source_node].get_weight(selected_pokemon.dest)
    total_time = time_to_reach_pokemon_source + time_to_run_over_the_pokemons_edge
    return selected_pokemon.value - total_time


def get_pokemon_src_and_dest_from_points(selected_pokemon, nodes):
    """
    The pokemons that we get from the server don't have a src and dest, so we will do it between 2 nodes
    """
    node1, node2 = nodes
    node1 = node1.id
    node2 = node2.id
    pokemon_src = None
    pokemon_dest = None
    if selected_pokemon.type > 0:  # if src < dest (that means the type is a positive number)
        pokemon_src = min(node1, node2)
        pokemon_dest = max(node1, node2)
    else:  # if src > dest (that means the type is a negative number)
        pokemon_src = max(node1, node2)
        pokemon_dest = min(node1, node2)

    return pokemon_src, pokemon_dest


def is_pokemon_on_the_edge_of_2_points(selected_pokemon, points):
    """
    checks if the pokemon is between two nodes, we do that by checking if the pos of the pokemon is on the
    Straight Equation between 2 nodes
    """
    pokemon_x = selected_pokemon.pos.x
    pokemon_y = selected_pokemon.pos.y
    pokemon_x = float(pokemon_x)
    pokemon_y = float(pokemon_y)
    x_coords, y_coords, _ = zip(*points)
    my_v = vstack([x_coords, ones(len(x_coords))]).T
    m, c = lstsq(my_v, y_coords, rcond=None)[0]

    try:
        assert_almost_equal(pokemon_y, pokemon_x * m + c)
        return True
    except AssertionError:
        return False


def move_agent(agent, next_node):
    """
    decide the next node that the agent will go to
    """
    client.choose_next_edge(
        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')


def add_agent(initial_node):
    """
    adds the agents from the server
    """
    client.add_agent("{\"id\":" + str(initial_node) + "}")


def pokemon_is_being_caught(selected_pokemon, selected_agents):
    """
    checks if the pokemon has an agent assigned that is coming to catch him
    """
    for agent in selected_agents:
        if agent.is_catching is not None:
            agents_pokemon_pos = agent.is_catching.pos
            pokemon_pos = selected_pokemon.pos
            if agents_pokemon_pos.x == pokemon_pos.x and agents_pokemon_pos.y == pokemon_pos.y:
                return True
    return False


pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons

pokemons = [p.Pokemon for p in pokemons]
for p in pokemons:
    x, y, _ = p.pos.split(',')
    p.pos = SimpleNamespace(x=float(x), y=float(y))

for pokemon in pokemons:
    src, dest = get_pokemon_src_and_dest_from_points(pokemon, calculate_pokemons_location(pokemon))
    pokemon.src = src
    pokemon.dest = dest

info = json.loads(client.get_info(), object_hook=lambda d: SimpleNamespace(**d)).GameServer

numberOfAgents = int(info.agents)

pokemons.sort(key=lambda p: p.value, reverse=True)  # sort the pokemons in reverse by value

for index in range(numberOfAgents):
    """
    decide the starting node of an agent
    """
    add_agent(pokemons[index].src)

client.start()

lastTime = time.time()

agent_to_agent_obj = {}
pokemon_to_pokemon_obj = {}

# --------------------------------------------Start of the game loop----------------------------------------------------

while client.is_running() == 'true':
    """
    The loop of the game
    """
    pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), my_x_scale=True), y=my_scale(float(y), my_y_scale=True))
    agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents

    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), my_x_scale=True), y=my_scale(float(y), my_y_scale=True))

    # check events
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:  # If the 'Stop' button was pressed, "gently" stop the program
            if exit_button.is_over(pos):
                client.stop_connection()
                pygame.quit()
                exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw info on the graph
    # create a text surface object,
    # on which text is drawn on it.
    ttl = str(int((int(client.time_to_end()) / 1000) % 60))
    info_text = info_font.render(client.get_info(), True, (255, 255, 255))
    ttl_text = info_font.render('Time left: ' + ttl, True, (255, 255, 255))

    # create a rectangular object for the
    # text surface object
    text_info_rect = info_text.get_rect()
    text_ttl_rect = ttl_text.get_rect()

    # set the center of the rectangular object.
    text_info_rect.center = (515, 10)
    text_ttl_rect.center = (87, 30)

    # get the info from the graph and draw it on the screen
    info_to_print = client.get_info()
    screen.blit(info_text, text_info_rect)
    screen.blit(ttl_text, text_ttl_rect)

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, my_x_scale=True)
        y = my_scale(n.pos.y, my_y_scale=True)

        # It's just to get a nice antialiasing circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, my_x_scale=True)
        src_y = my_scale(src.pos.y, my_y_scale=True)
        dest_x = my_scale(dest.pos.x, my_x_scale=True)
        dest_y = my_scale(dest.pos.y, my_y_scale=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)

    # draw Pokemon
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    exit_button.draw(screen)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons

    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=float(x), y=float(y))

    for pokemon in pokemons:
        """
        Set the src and dest of the pokemons
        """
        src, dest = get_pokemon_src_and_dest_from_points(pokemon, calculate_pokemons_location(pokemon))
        pokemon.src = src
        pokemon.dest = dest

    for agent in agents:
        agent.is_catching = None

    for agent in agents:
        """
        The complete algo for the agent for the choosing the next node for the agent to go to
        """
        if agent_to_agent_obj.get(agent.id) is None:
            agent_to_agent_obj[agent.id] = Agent(agent.id, agent.value, agent.src, agent.dest, agent.speed, agent.pos)
        else:
            current_agent_obj = agent_to_agent_obj.get(agent.id)
            current_agent_obj.src = agent.src
            current_agent_obj.dest = agent.dest
            current_agent_obj.value = agent.value
            current_agent_obj.speed = agent.speed
        agent_obj = agent_to_agent_obj.get(agent.id)
        agent.is_catching = agent_obj.is_catching
        if agent_obj.dest == -1:
            best_pokemon = None
            if agent_obj.is_catching is None:
                best_juice = None
                for pokemon in pokemons:
                    if not pokemon_is_being_caught(pokemon, agents):  # is the pokemon is not being caught
                        current_juice = calculate_juiciness(agent_obj, pokemon)
                        if best_juice is None or current_juice > best_juice:
                            best_juice = current_juice
                            best_pokemon = pokemon
                if best_pokemon is not None:
                    agent_obj.is_catching = best_pokemon
                    best_pokemon.isBeingCaught = True
                    _, agent_obj.path = myGraphAlgo.shortest_path(agent_obj.src, best_pokemon.src)
            best_pokemon = agent_obj.is_catching
            if agent_obj.is_catching is not None:
                if len(agent_obj.path) > 0 and agent_obj.src == agent_obj.path[0]:
                    agent_obj.path.pop(0)
                if len(agent_obj.path) > 0:
                    move_agent(agent_obj, agent_obj.path[0])
                elif agent_obj.src == best_pokemon.src:
                    move_agent(agent_obj, best_pokemon.dest)
                else:
                    agent_obj.is_catching = None
            print("Time to end: " + ttl, client.get_info())

    time.sleep(0.1)
    client.move()

