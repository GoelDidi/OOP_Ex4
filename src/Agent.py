class Agent:
    """This class represents the Agents who catch the pokemons"""
    def __init__(self, agent_id=None, value=None, src=None, dest=None, speed=None, pos=None):
        self.id = agent_id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.is_catching = None

    def set_src(self, src):
        self.src = src

    def set_dest(self, dest):
        self.dest = dest

    def is_moving(self):
        return self.dest != -1

    def set_is_catching(self, is_catching):
        self.is_catching = is_catching
