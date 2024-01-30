import Evaluaotr


def jaccard_distance(sentence1, sentence2):
    tks1 = list(set(sentence1.split(' ')))
    tks2 = list(set(sentence2.split(' ')))

    count = 0
    for tk in tks1:
        if tk in tks2:
            count += 1

    result = list(set(tks1) | set(tks2))
    result2 = list(set(tks1) & set(tks2))

    # print(tks1)
    # print(tks2)
    # print(result)
    # print(result2)
    if len(result) == 0:
        return 0
    return count / len(result)


class RewardUtil:
    def __init__(self, device=None):
        self.evaluator = Evaluaotr.Evaluator(device=device)

    def get_reward(self, query1, query2):
        reward1 = self.evaluator.propagate(query1, query2)[0]
        reward2 = 1 - jaccard_distance(query1, query2)
        if reward1 < 0:
            return reward1
        else:
            return reward2
        # print('reward1', reward1, 'reward2', reward2)
        # print('query1', query1, 'query2', query2)
        # print(reward1, reward2)
        # input()
