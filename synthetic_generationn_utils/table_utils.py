import random
import re
import numpy as np
import pandas as pd
import spacy


nlp = spacy.load("en_core_web_sm")


def convert_table2d_to_table(table_2d):
    table = {}
    num_col = len(table_2d[0])
    for c in range(num_col):
        cols = []
        for r in range(1, len(table_2d)):
            cols.append(str(table_2d[r][c]))
        table[table_2d[0][c]] = cols
    table = pd.DataFrame.from_dict(table)
    return table


def check_person_entity(word):
    doc = nlp(str(word))
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return True
    return False


def check_date_entity(word):
    doc = nlp(str(word))
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            return True
    return False


def is_num(word):
    try:
        float(extract_numbers(word))
        return True
    except:
        return False


def extract_numbers(text):
    # 정규표현식 패턴 설정
    pattern = r'\d+'

    # 정규표현식을 사용하여 숫자 추출
    numbers = re.findall(pattern, text)
    word = numbers[0]

    try:
        return float(word)
    except:
        return 0.0


def extract_numbers_(s):
    word = ''.join(re.findall(r'\d+(\.\d+)?', s))
    try:
        return float(word)
    except:
        return 0.0


def arg_sort(sequence):
    arr = np.array(sequence)
    return np.argsort(arr)


def most_frequent_value(my_list):
    frequency_dict = {}

    # 빈도 계산
    for item in my_list:
        if item in frequency_dict:
            frequency_dict[item] += 1
        else:
            frequency_dict[item] = 1

    # 가장 빈번한 요소 찾기
    most_common_element = max(frequency_dict, key=frequency_dict.get)
    return most_common_element


def average(values):
    return sum(values) / len(values)


def median(values):
    arg_indices = arg_sort(values)
    if len(values) % 2 == 0:
        m = [int(len(values) / 2) - 1, int(len(values) / 2)]
        median_value = (values[arg_indices[m[0]]] + values[arg_indices[m[1]]]) / 2
    else:
        m = int(len(values) / 2)
        median_value = values[arg_indices[m]]
    return median_value


def median_column(table_2d, column_index):
    c = column_index

    column_values = []
    for r in range(len(table_2d)):
        column_values.append(table_2d[r][c])

    arg_indices = arg_sort(column_values)

    if len(table_2d) % 2 == 0:
        m = [int(len(table_2d)), int(len(table_2d)) + 1]
        median_value = (table_2d[arg_indices[m[0]]][c] + table_2d[arg_indices[m[1]]][c]) / 2
    else:
        m = int(len(table_2d)) + 1
        median_value = table_2d[arg_indices[m]][c]
    return median_value


def check_single_number(text):
    text = str(text)

    pattern = r'(\d+(\.\d+)?)([a-zA-Z]+)?'
    if re.fullmatch(pattern, text):
        return True
    else:
        return False


def check_single_number_strict(text):
    text = str(text)

    try:
        float(text)
        return True
    except:
        return False


def check_numeric_column(table_2d, column_index):
    for r in range(1, len(table_2d)):
        c = column_index

        if check_single_number(table_2d[r][c]) is False:
            return False
    return True


def check_numeric_column_strict(table_2d, column_index):
    for r in range(1, len(table_2d)):
        c = column_index

        if check_single_number_strict(table_2d[r][c]) is False:
            return False
    return True


def get_numeric_column(table_2d):
    column_indices = []

    for c in range(len(table_2d[0])):
        check = check_numeric_column(table_2d=table_2d, column_index=c)
        check2 = check_sequential_column(table_2d=table_2d, column_index=c)

        if check is True and check2 is False:
            column_indices.append(c)

    return column_indices


def get_numeric_column_strict(table_2d):
    column_indices = []

    for c in range(len(table_2d[0])):
        check = check_numeric_column_strict(table_2d=table_2d, column_index=c)
        check2 = check_sequential_column(table_2d=table_2d, column_index=c)

        if check is True and check2 is False:
            column_indices.append(c)

    return column_indices


def check_sequential_column(table_2d, column_index):
    check = True

    for r in range(2, len(table_2d)):
        # print(r, len(table_2d), len(table_2d[r]), len(table_2d[r-1]))
        if is_num(table_2d[r][column_index]) is False or is_num(table_2d[r - 1][column_index]) is False:
            return False
        # print('check:', abs(extract_numbers(table_2d[r][column_index]) - extract_numbers(table_2d[r - 1][column_index])))
        if abs(extract_numbers(table_2d[r][column_index]) - extract_numbers(table_2d[r - 1][column_index])) != 1:
            check = False
    return check


def check_table_length(table_2d):
    for r in range(len(table_2d) - 1):
        if len(table_2d[r]) != len(table_2d[r + 1]):
            return False
    return True


def find_sequential_column(table_2d):
    column_index = -1

    for c in range(len(table_2d[0])):
        check = check_sequential_column(table_2d=table_2d, column_index=c)
        if check is True:
            column_index = c

    return column_index


def remove_column(table_2d, column_index):
    for r in range(len(table_2d)):
        tr = table_2d[r]
        tr.pop(column_index)

    return table_2d


def convert_table_for_synthetic_generation(table_2d):
    new_table_2d = []

    for r in range(len(table_2d)):
        new_table_2d.append(table_2d[r][:])

    for c in range(len(table_2d[0])):
        if check_numeric_column(table_2d=table_2d, column_index=c) is True:
            for r in range(1, len(table_2d)):
                value = extract_numbers(table_2d[r][c])
                new_table_2d[r][c] = value
    return new_table_2d


def convert_table_for_hierarchical(table_2d):
    seq_column = find_sequential_column(table_2d=table_2d)
    if seq_column != -1:
        remove_column(table_2d=table_2d, column_index=seq_column)

    numeric_columns = get_numeric_column_strict(table_2d=table_2d)
    if len(table_2d[0]) - len(numeric_columns) == 0 or len(numeric_columns) < 2 or len(table_2d) < 4:
        return None

    while True:
        numeric_columns = get_numeric_column_strict(table_2d=table_2d)
        if len(table_2d[0]) - len(numeric_columns) == 1:
            break

        check = True
        for c in list(reversed(range(table_2d[0]))):
            if c not in numeric_columns:
                remove_column(table_2d=table_2d, column_index=c)
                break
            check = False

        if check is False:
            break

    return table_2d


def make_hierarchical_table(table_2d):
    None


if __name__ == "__main__":
    # 사용 예
    print(extract_numbers('0asd  asd 0.12312'))
    print(check_single_number('a11'))