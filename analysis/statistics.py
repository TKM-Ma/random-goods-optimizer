import numpy as np

class Statistics:
    @staticmethod
    def mean(group):
        scores = np.array([item.score for item in group.items])
        return np.mean(scores)
    
    @staticmethod
    def var(group):
        scores = np.array([item.score for item in group.items])
        return np.var(scores)

    @staticmethod
    def hit_rate(group, threshold):
        scores = np.array([item.score for item in group.items])
        return np.mean(scores >= threshold)