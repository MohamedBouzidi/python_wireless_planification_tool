class Serializable:

    def __init__(self):
        pass

    def save(self, file):
        raise NotImplementedError("save() should be implemented")

    def load(self, file):
        raise NotImplementedError("load() should be implemented")