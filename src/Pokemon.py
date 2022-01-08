class Pokemon:
    """This class represents the Pokemons on the graph"""
    def __init__(self, value: float = None, pokemon_type: int = None, pos: str = None, is_being_caught=False):
        self.value = value
        self.type = pokemon_type
        split_pos = pos.split(",")
        self.x = float(split_pos[0])
        self.y = float(split_pos[1])
        self.z = float(split_pos[2])
        self.src = None
        self.dest = None
        self.initialJuice = None
        self.is_being_caught = is_being_caught

    def set_src(self, src):
        self.src = src

    def set_dest(self, dest):
        self.dest = dest

    def set_initial_juice(self, initial_juice):
        self.initialJuice = initial_juice

    def set_is_being_caught(self, is_being_caught):
        self.is_being_caught = is_being_caught
