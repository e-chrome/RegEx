from pprint import pprint
import re
import csv

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", 'r', newline='', encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
# создаем паттерны
pattern_full_name = re.compile(r'([А-ЯЁ]\w+)\W+([А-ЯЁ]\w+)\W+([А-ЯЁ]\w+)')
pattern_short_name = re.compile(r'([А-ЯЁ]\w+)\W+([А-ЯЁ]\w+)')
pattern_organization = re.compile(r'([А-ЯЁ]\w+)')
pattern_phone = re.compile(r'(\+7|8)\s?(\([\d]+\))?\s?([\d|\-]+)([\s\(]*)(доб)?[\s.]*([\d]+)?[)]?')
pattern_email = re.compile(r'[^\,\s]+[@]\w+\.\w+')

correct_list = []
contacts_list.pop(0)
item_list = []

# преобразуем вложенные списки в строки путем сшивания
for contact in contacts_list:
    item = ''
    for note in contact:
        item += note + ', '
    item_list.append(item)

# ищем паттерны в строках, заносим найденные значения в словарь
for item in item_list:
    contact_dict = {
        'lastname': '',
        'firstname': '',
        'surname': '',
        'organization': '',
        'position': '',
        'phone': '',
        'email': ''
    }

    if pattern_full_name.search(item):
        contact_dict['lastname'] = pattern_full_name.search(item).group(1)
        contact_dict['firstname'] = pattern_full_name.search(item).group(2)
        contact_dict['surname'] = pattern_full_name.search(item).group(3)
        item = item.replace(pattern_full_name.search(item).group(0), '')
    elif pattern_short_name.search(item):
        contact_dict['lastname'] = pattern_short_name.search(item).group(1)
        contact_dict['firstname'] = pattern_short_name.search(item).group(2)
        contact_dict['surname'] = ''
        item = item.replace(pattern_short_name.search(item).group(0), '')

    if pattern_organization.search(item):
        contact_dict['organization'] = pattern_organization.search(item).group(1)
        item = item.replace(pattern_organization.search(item).group(0), '')

    if pattern_phone.search(item):
        prefix = '+7'
        if pattern_phone.search(item).group(2):
            code = pattern_phone.search(item).group(2)
            dirty_number = pattern_phone.search(item).group(3)
            number = dirty_number.replace('-', '')
            number = number[0:3] + '-' + number[3:5] + '-' + number[5:7]
        else:
            code = '(' + pattern_phone.search(item).group(3)[0:3] + ')'
            dirty_number = pattern_phone.search(item).group(3)[3:]
            number = dirty_number.replace('-', '')
            number = number[0:3] + '-' + number[3:5] + '-' + number[5:7]
        if pattern_phone.search(item).group(6):
            additional = ' доб.' + pattern_phone.search(item).group(6)

        else:
            additional = ''
        phone = prefix + code + number + additional
        contact_dict['phone'] = phone
        item = item.replace(pattern_phone.search(item).group(0), '')

    if pattern_email.search(item):
        contact_dict['email'] = pattern_email.search(item).group(0)
        item = item.replace(pattern_email.search(item).group(0), '')

    item = item.replace(',', '')
    contact_dict['position'] = item.strip()

    correct_list.append(contact_dict)

# объединяем дубликаты контактов
index_of_double = []
for i in range(len(correct_list)):
    for j in range(i+1, len(correct_list)):
        if correct_list[i]['firstname'] == correct_list[j]['firstname'] and \
                correct_list[i]['lastname'] == correct_list[j]['lastname']:
            for key in correct_list[i].keys():
                if correct_list[i][key] == '':
                    correct_list[i][key] = correct_list[j][key]
            index_of_double.append(j)

final_list = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']]

# удаляем дубликаты контактов, преобразуем словарь в список в нужной последовательности
for i in range(len(correct_list)):
    if i not in index_of_double:
        person = []
        person.append(correct_list[i]['lastname'])
        person.append(correct_list[i]['firstname'])
        person.append(correct_list[i]['surname'])
        person.append(correct_list[i]['organization'])
        person.append(correct_list[i]['position'])
        person.append(correct_list[i]['phone'])
        person.append(correct_list[i]['email'])
        final_list.append(person)

pprint(final_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(final_list)