from models import group
from analysis.statistics import Statistics

class Optimizer:
    @staticmethod
    def recommend(groups, budget):
        scores = {}
        recommend = {}
        for group in groups:
            scores[group] = Optimizer.cal_score(group)
            recommend[group] = 0
        
        for i in range(budget):
            best_group = max(scores, key=scores.get)
            recommend[best_group]+= 1
            scores[best_group] = Optimizer.cal_score(best_group, recommend)
        
        return recommend
    
    @staticmethod
    def cal_score(group, recommend=None):
        lambda_ = 0.1
        mean = Statistics.mean(group)
        var = Statistics.var(group)
        score = mean - lambda_ * var + 5 * Statistics.hit_rate(group, 8) + 3 * Statistics.hit_rate(group, 10)

        if recommend != None:
            alpha = 0.1
            score /= 1 + alpha * recommend[group]
        return score