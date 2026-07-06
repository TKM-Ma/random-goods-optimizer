from .statistics import Statistics

class Optimizer:
    LAMBDA = 0.1
    ALPHA = 0.05
    
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
        scores = Statistics.scores(group)
        mean = Statistics.mean(scores)
        var = Statistics.var(scores)
        score = mean - Optimizer.LAMBDA * var + 7 * Statistics.hit_rate(scores, 8) + 3 * Statistics.hit_rate(scores, 10)

        if recommend != None:
            score /= 1 + Optimizer.ALPHA * recommend[group]
        return score