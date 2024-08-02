def discriminant(a, b, c):
    """
    функция для нахождения дискриминанта
    Параметры: a, b, c - коэффициенты квадратного уравнения
    """
    return b ** 2 - 4 * a * c


def solution(a, b, c):
    """
    функция для нахождения корней уравнения в зависимости от дискриминанта
    Параметры: a, b, c - коэффициенты квадратного уравнения
    """
    D = discriminant(a, b, c)
    if D < 0:
        print("корней нет")
        return None
    elif D == 0:
        return -b / (2 * a)
    else:
        return (-b + D ** 0.5) / (2 * a), (-b - D ** 0.5) / (2 * a)
