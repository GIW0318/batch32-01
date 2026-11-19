class CooldownTracker:
    def __init__(self, abilities):
        self.abilities = abilities

    def cast(self, name, now):
        return None

    def advance(self, now):
        return None

    def ready(self, name, now):
        return None

    def state(self):
        return {}
