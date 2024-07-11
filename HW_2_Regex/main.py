import re
import csv


def standardize_phone(phone_num: str) -> str:
    pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]*(\d{2})\s*\(?\w*\.?\s*(\d*)\)?"
    match = re.search(pattern, phone_num)
    res_number = ''
    if match:
        res_number = f'+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}'
        if match.group(6):
            res_number += f' доб.{match.group(6)}'
    return res_number


def combine_persons(contact: list, uniq_persons: dict) -> None:
    lastname, name = [value.strip().lower() for value in contact[:2]]
    person = tuple([lastname, name])
    if person not in uniq_persons:
        uniq_persons[person] = contact
    else:
        for ind, item in enumerate(contact):
            if not uniq_persons[person][ind]:
                uniq_persons[person][ind] = item


def main():
    with open('phonebook_raw.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        contacts_list = list(reader)
    title = contacts_list[0]
    edited_contacts_list = []
    uniq_persons_long_dict = {}
    uniq_persons_short_dict = {}
    for contact in contacts_list[1:]:
        splitted_name = ' '.join(contact[0:3]).split()
        for i in range(len(splitted_name)):
            contact[i] = splitted_name[i]
        cur_phone = str(contact[-2])
        surname = contact[3]
        contact[-2] = standardize_phone(cur_phone)
        if surname:
            combine_persons(contact, uniq_persons_long_dict)
        else:
            combine_persons(contact, uniq_persons_short_dict)
    for contact in uniq_persons_short_dict.values():
        combine_persons(contact, uniq_persons_long_dict)
    edited_contacts_list.append(title)
    for con in uniq_persons_long_dict.values():
        edited_contacts_list.append(con)
    with open('phonebook.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(edited_contacts_list)


if __name__ == '__main__':
    main()
