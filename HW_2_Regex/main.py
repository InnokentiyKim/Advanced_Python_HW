import re
import csv
from pprint import pprint


def standardize_phone(phone_num: str) -> str:
    pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]*(\d{2})\s*\(?\w*\.?\s*(\d*)\)?"
    match = re.search(pattern, phone_num)
    res_number = ''
    if match:
        res_number = f'+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}'
        if match.group(6):
            res_number += f' доб.{match.group(6)}'
    return res_number


def main():
    with open('phonebook_raw.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        contacts_list = list(reader)
    title = contacts_list[0]
    edited_contacts_list = []
    uniq_person_dict = {}
    for contact in contacts_list[1:]:
        splitted_name = ' '.join(contact[0:3]).split()
        contact[0:3] = splitted_name
        cur_phone = str(contact[-2])
        contact[-2] = standardize_phone(cur_phone)
        person = tuple(contact[:2])
        if person not in uniq_person_dict:
            uniq_person_dict[person] = contact
        else:
            for ind, item in enumerate(contact):
                if not uniq_person_dict[person][ind]:
                    uniq_person_dict[person][ind] = item
    edited_contacts_list.append(title)
    for con in uniq_person_dict.values():
        edited_contacts_list.append(con)
    pprint(edited_contacts_list)
    with open('phonebook.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(edited_contacts_list)


if __name__ == '__main__':
    main()
