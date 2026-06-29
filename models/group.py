from analysis.statistics import Statistics

class Group:
    def __init__(self, name, items):
        self.name = name
        self.items = items
    
    def print_status(self):
        mean = Statistics.mean(self)
        var = Statistics.var(self)
        hit_rate = Statistics.hit_rate(self, 8)
        
        print("グループ:" + self.name)
        print(f"平均\t:{mean:.3}")
        print(f"分散\t:{var:.3}")
        print(f"当たり率:{hit_rate:.1%}")