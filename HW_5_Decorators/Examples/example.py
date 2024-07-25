from Loggers.logger import logger
import re


@logger("example.log")
def standardize_phone(phone_num: str) -> str:
    pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]*(\d{2})\s*\(?\w*\.?\s*(\d*)\)?"
    match = re.search(pattern, phone_num)
    res_number = ''
    if match:
        res_number = f'+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}'
        if match.group(6):
            res_number += f' доб.{match.group(6)}'
    return res_number
