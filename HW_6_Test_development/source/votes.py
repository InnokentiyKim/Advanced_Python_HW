votes_list_1 = [1, 1, 1, 2, 3]
votes_list_2 = [1, 2, 3, 2, 2]
votes_list_3 = []


def vote(votes):
    """
    Функция подсчета победителя голосования
    Параметры: votes - список голосов (list[int])
    Возвращает: победителя с максимальным количеством голосов (int)
    """
    max_count_num = 0
    for num in set(votes):
        if votes.count(num) > max_count_num:
            max_count_num = num
    return max_count_num
