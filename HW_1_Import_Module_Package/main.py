from application.salary import calculate_salary
from application.db.people import get_employees
import datetime
import numpy as np


print(f'Current date is {datetime.date.today()}')
if __name__ == '__main__':
    calculate_salary()
    get_employees()
    some_array = np.array(range(0, 101, 5))
    print(f'Some array: {some_array}')
    list_size = 5
    print(f'{list_size} random values from standart deviation: {np.random.standard_normal(size=list_size)}')

