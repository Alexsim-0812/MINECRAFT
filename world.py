import numpy as np
from noise import pnoise2

class WorldGenerator:
    def __init__(self, seed=0, scale=100.0):
        self.seed = seed
        self.scale = scale
        self.world_data = {}

    def generate_terrain(self, x, y, z, chunk_size=16):
        for i in range(chunk_size):
            for j in range(chunk_size):
                for k in range(chunk_size):
                    world_x = x * chunk_size + i
                    world_z = z * chunk_size + j
                    world_y = y * chunk_size + k
                    
                    noise_value = pnoise2(world_x / self.scale, world_z / self.scale, octaves=4, base=self.seed)
                    
                    if world_y < 5:
                        block_type = 'stone'
                    elif world_y < 10 and noise_value > 0.3:
                        block_type = 'dirt'
                    elif world_y == 10 and noise_value > 0.3:
                        block_type = 'grass'
                    elif world_y > 15 and noise_value < -0.3:
                        block_type = 'water'
                    elif world_y < 8 and noise_value > 0.5:
                        block_type = 'sand'
                    else:
                        block_type = 'air'
                    
                    if block_type != 'air':
                        self.world_data[(world_x, world_y, world_z)] = block_type
        
        return self.world_data

    def get_block(self, x, y, z):
        return self.world_data.get((x, y, z), 'air')

    def set_block(self, x, y, z, block_type):
        self.world_data[(x, y, z)] = block_type

    def remove_block(self, x, y, z):
        if (x, y, z) in self.world_data:
            del self.world_data[(x, y, z)]