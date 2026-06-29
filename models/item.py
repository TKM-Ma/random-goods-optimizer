class Item:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def to_string(self):
        return self.name