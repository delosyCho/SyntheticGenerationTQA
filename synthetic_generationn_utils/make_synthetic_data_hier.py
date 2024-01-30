import random

from table_utils import get_numeric_column, convert_table_for_synthetic_generation, convert_table_for_hierarchical, check_table_length
from transformers import AutoTokenizer, TapasTokenizer

import numpy as np

import table_utils

import pandas as pd

from hierarchical_table_utils import HierarchicalExpressionObject

check1 = 0
check2 = 0
check3 = 0
check4 = 0
check5 = 0

count = 0

total = 2000000

answer_length = 128
max_length = 1024
max_answer = 128

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")

input_ids = np.zeros(shape=[total, max_length], dtype=np.int32)
attention_mask = np.zeros(shape=[total, max_length], dtype=np.int16)
label_ids = np.full(shape=[total, answer_length], fill_value=-100, dtype=np.int32)

for d in range(1, 10):
    data_number = d
    data_number = str(data_number)

    file = open('tapas_data/splited_tapas_{}.txt'.format(data_number), 'r', encoding='utf-8')

    whole_text = file.read()

    table_line = whole_text.split('\n\n')

    print(len(table_line))

    for i in range(len(table_line)):
        if i % 1000 == 0:
            print(i, '/', len(table_line), 'count:', count, 'check:', check1, check2, check3, check4, check5)

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
            check1 += 1
            continue

        if len(table_data) * len(table_data[0]) > 256:
            check2 += 1
            continue

        if check_table_length(table_2d=table_data) is False:
            check3 += 1
            continue

        try:
            numeric_column_indexes = get_numeric_column(table_2d=table_data)
            if len(numeric_column_indexes) >= 3 and len(table_data) > 6 and check_table_length(table_2d=table_data) is True:
                None
            else:
                continue
            table_data = convert_table_for_hierarchical(table_2d=table_data)
            table_data = convert_table_for_synthetic_generation(table_2d=table_data)

        except:
            continue
        # expression_object = HierarchicalExpressionObject(table_2d=table_data)

        for _ in range(100):
            try:
                if True:
                    c = 0
                    while True:
                        expression_object = HierarchicalExpressionObject(table_2d=table_data)
                        if expression_object is not None or c > 100:
                            break
                        c += 1
                    # print('1')
                    if expression_object is None:
                        check4 += 1
                        continue

                    table_2d = expression_object.new_table_2d

                    sentences = expression_object.sentences
                    query = expression_object.natural_statement
                    answer_statement = expression_object.logic_statement

                    tokens = []
                    tokens.append('<s>')

                    query_tokens = tokenizer.tokenize(query)
                    tokens.extend(query_tokens)
                    tokens.append('</s>')

                    for sentence in sentences:
                        sentence_tokens = tokenizer.tokenize(sentence)
                        tokens.extend(sentence_tokens)
                        tokens.append('</s>')

                    for r, tr in enumerate(table_2d):
                        row_statement = 'row ' + str(r) + ' :'
                        statement_tokens = tokenizer.tokenize(row_statement)
                        tokens.extend(statement_tokens)

                        for td in tr:
                            if td is not None:
                                td_tokens = tokenizer.tokenize(str(td))
                                tokens.extend(td_tokens)
                                tokens.append('</s>')

                    length = min(max_length, len(tokens))
                    if length == max_length:
                        tokens[length - 1] = '</s>'

                    ids = tokenizer.convert_tokens_to_ids(tokens=tokens)

                    for j in range(length):
                        input_ids[count, j] = ids[j]
                        attention_mask[count, j] = 1

                    inputs = tokenizer(answer_statement, return_tensors="np")
                    ids = list(inputs['input_ids'][0, :])
                    length = min(len(ids), answer_length)
                    label_ids[count, 0: length] = ids[0: length]
                    count += 1

            except:
                # check4 += 1
                continue


np.save('input_ids_hierarchical', input_ids[:count])
np.save('attention_mask_hierarchical', attention_mask[:count])
np.save('label_ids_hierarchical', label_ids[:count])





