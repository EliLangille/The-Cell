from Item import Item


class Key(Item):
    def __init__(self, name, description, lock_id):
        super().__init__(name, description, damage=1)
        self.lock_id = lock_id

    def get_lock(self):
        return self.lock_id
