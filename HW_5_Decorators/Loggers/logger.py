import os
from functools import wraps
from datetime import datetime


def simple_logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        cur_date = datetime.now()
        result = old_function(*args, **kwargs)
        file_name = 'main.log'
        res = str(cur_date) + ' - ' + str(old_function.__name__) + ' - ' + str(args) + ' - ' + str(kwargs) + ' - ' + str(result) + '\n'
        with open(file_name, 'a+') as file:
            file.write(res)
        return result
    return new_function


def logger(path='main.log'):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            cur_date = datetime.now()
            result = old_function(*args, **kwargs)
            file_name = str(path)
            res = str(cur_date) + ' - ' + str(old_function.__name__) + ' - ' + str(args) + ' - ' + str(kwargs) + ' - ' + str(result) + '\n'
            with open(file_name, 'a+') as file:
                file.write(res)
            return result
        return new_function
    return __logger