from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise

app = Ursina()

# Load textures and other assets
textures = {
    'grass': load_texture('assets/grass_block.png'),
    'stone': load_texture('assets/stone_block.png'),
    'brick': load_texture('assets/brick_block.png'),
    'dirt': load_texture('assets/dirt_block.png')
}

arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
block_pick = 'grass'  # Use texture name instead of an index

# Create Perlin noise object
noise = PerlinNoise(octaves=2, seed=4)

# Constants
CHUNK_SIZE = 32
TERRAIN_WIDTH = 20
TERRAIN_DEPTH = 20
TERRAIN_HEIGHT = 8

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=textures['grass']):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )

    def input(self, key):
        global block_pick
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                voxel = Voxel(position=self.position + mouse.normal, texture=textures[block_pick])

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

def generate_terrain():
    terrain = []
    for x in range(TERRAIN_WIDTH):
        for z in range(TERRAIN_DEPTH):
            y = int((noise([x/50, z/50]) + 1) * (TERRAIN_HEIGHT / 2))
            for i in range(y):
                if i == 0:
                    terrain.append(Voxel(position=(x, 0, z), texture=textures['stone']))
                else:
                    terrain.append(Voxel(position=(x, i, z), texture=textures['grass']))
    return terrain

# Generate terrain in chunks
for x_chunk in range(0, TERRAIN_WIDTH, CHUNK_SIZE):
    for z_chunk in range(0, TERRAIN_DEPTH, CHUNK_SIZE):
        chunk = generate_terrain()
        for voxel in chunk:
            voxel.position += (x_chunk, 0, z_chunk)

# Chunk management (not necessary for rendering but can be used for optimization)
chunks = {}

def get_chunk_key(position):
    return int(position[0] // CHUNK_SIZE), int(position[2] // CHUNK_SIZE)

def update():
    global block_pick
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']:
        block_pick = 'grass'
    elif held_keys['2']:
        block_pick = 'stone'
    elif held_keys['3']:
        block_pick = 'brick'

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Pause handling
pause_handler = Entity(ignore_paused=True)
def pause_handler_input(key):
    global player
    if key == 'escape':
        application.paused = not application.paused
        pause_text.enabled = application.paused
        window.show_cursor = not window.show_cursor
        player.enabled = not player.enabled
        if not application.paused:
            window.show_cursor = False

pause_handler.input = pause_handler_input

player = FirstPersonController()
hand = Hand()
sky = Sky(texture='sky.png')

app.run()
