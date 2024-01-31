import random

from table_utils import check_numeric_column, check_sequential_column, get_numeric_column, convert_table_for_synthetic_generation, check_table_length
from transformers import AutoTokenizer, TapasTokenizer

import numpy as np

from synthesize_utils import ExpressionObject, RandomQueryExpression, permutate_logic

count = 0
total = 500000

query_file = open('synthetic_queries.txt', 'w', encoding='utf-8')

for d in range(1, 10):
    data_number = d
    data_number = str(data_number)

    file = open('tapas_data/splited_tapas_{}.txt'.format(data_number), 'r', encoding='utf-8')

    whole_text = file.read()

    table_line = whole_text.split('\n\n')

    print(len(table_line))

    if count + 100 >= total:
        break

    for i in range(len(table_line)):
        if count + 100 >= total:
            break

        if i % 1000 == 0:
            print(i, '/', len(table_line), 'count:', count, 'check:',)

        try:
            tks = table_line[i].split('table {')

            table_text = tks[1].split(' questions {')[0]
            columns = table_text.split('columns')
            columns.pop(0)

            rows = columns.pop(-1).split('rows')
            columns.append(rows.pop(0))

            table_data = []

            for c in range(len(columns)):
                column = columns[c].split('text: "')[1].split('" }')[0]
                columns[c] = column
            table_data.append(columns)

            for r in range(len(rows)):
                cells = rows[r].split('cells {')
                cells.pop(0)
                for c in range(len(cells)):
                    # print('-----')
                    # print(rows[r])
                    # print(cells)
                    # print(c, len(cells), cells[c])
                    cell = cells[c].split(' text: "')[1].split('" }')[0]
                    cells[c] = cell

                table_data.append(cells)
        except:
            continue

        check = True
        for c in range(len(table_data[0])):
            if len(table_data[0][c]) < 2:
                check = False
                break
        if check is False:
            continue

        if len(table_data) * len(table_data[0]) > 256:
            continue

        if check_table_length(table_2d=table_data) is False:
            continue

        for _ in range(3):
            try:
                numeric_column_indexes = get_numeric_column(table_2d=table_data)
                if len(numeric_column_indexes) >= 3 and len(table_data) > 3 and check_table_length(table_2d=table_data) is True:
                    table_2d = convert_table_for_synthetic_generation(table_2d=table_data)

                    c = 0
                    if random.randint(0, 1) == 0:
                        while True:
                            expression_object = ExpressionObject(table_2d=table_2d)
                            if expression_object is not None or c > 100:
                                break
                            c += 1

                    else:
                        while True:
                            expression_object = RandomQueryExpression(table_2d=table_2d)
                            if expression_object is not None or c > 100:
                                break
                            c += 1

                    if expression_object is None:
                        continue

                    sentences = expression_object.sentences
                    query = expression_object.natural_statement
                    query_ = permutate_logic(query)
                    query_file.write(query + '\t' + query_ + '\n')
                    count += 1
            except:
                None

query_file.close()