class TerrainQuadtree:
    def __init__(self, max_lod=3, budget=8):
        self.max_lod = max_lod
        self.budget = budget
        self.patches = {}

    def add_patch(self, patch_id, x, y, size, neighbors=None):
        return None

    def select(self, camera, previous=None):
        return []
