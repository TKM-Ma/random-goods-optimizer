import numpy as np

class Statistics:
    @staticmethod
    def scores(group):
        return np.array([item.score for item in group.items])

    @staticmethod
    def mean(scores):
        return np.mean(scores)
    
    @staticmethod
    def var(scores):
        return np.var(scores)

    @staticmethod
    def hit_rate(scores, threshold):
        return np.mean(scores >= threshold)
    
    @staticmethod
    def find_unrated_items(groups):
        unrated = []

        for group in groups:
            for item in group.items:
                if item.score == 0:
                    unrated.append((group.name, item.name))

        return unrated