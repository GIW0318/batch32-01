class ConstraintSolver:
    def __init__(self, iterations=4):
        self.iterations = iterations
        self.bodies = {}
        self.contacts = []

    def add_body(self, body_id, mass, x, y, vx=0.0, vy=0.0, static=False):
        return None

    def add_contact(self, a, b, nx, ny, penetration, restitution=0.0, friction=0.0):
        return None

    def step(self, dt):
        return None

    def state(self):
        return {}
