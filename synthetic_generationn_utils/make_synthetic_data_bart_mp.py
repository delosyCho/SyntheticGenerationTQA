from multiprocessing import Pool

import random

from table_utils import check_numeric_column, check_sequential_column, get_numeric_column, \
    convert_table_for_synthetic_generation, check_table_length
from transformers import AutoTokenizer, TapasTokenizer

import numpy as np

import table_utils

import pandas as pd

from synthesize_utils import ExpressionObject, RandomQueryExpression

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


check1 = 0
check2 = 0
check3 = 0
check4 = 0
check5 = 0

count = 0

total = 1000000

answer_length = 128
max_length = 1024
max_answer = 128


table_lines = np.zeros(shape=[total], dtype='<U3000')

total_count = 0
# table_line = []
for d in range(1, 2):
    data_number = d
    data_number = str(data_number)

    file = open('tapas_data/splited_tapas_{}.txt'.format(data_number), 'r', encoding='utf-8')

    whole_text = file.read()

    table_line_ = whole_text.split('\n\n')
    for line in table_line_:
        try:
            tks = line.split('table {')
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

            lines = []
            for tr in table_data:
                line = '[td]'.join(tr)
                lines.append(line)
            table_text_flat = '[tr]'.join(lines)

        except:
            continue

        # print(len(line), len(line) < 3000)
        if len(table_text_flat) < 3000:
            table_lines[total_count] = table_text_flat
            total_count += 1

    print(total_count, len(table_line_))
total = total_count

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")


def process_data(i):
    # if count + 100 >= total:
    #     break

    # if i % 1000 == 0:
    #     print(i, '/', len(table_line), 'count:', count, 'check:', check1, check2, check3, check4, check5)
    # if i % 1000 == 0:
    #     print(i)
    try:
        table_text = table_lines[i]
        lines = table_text.split('[tr]')

        table_data = []
        for line in lines:
            tks = line.split('[td]')
            table_data.append(tks)

    except:
        return None

    if len(table_data) * len(table_data[0]) > 256:
        return None

    if check_table_length(table_2d=table_data) is False:
        return None

    result = []

    for _ in range(50):
        try:
            input_ids = np.zeros(shape=[1, max_length], dtype=np.int32)
            attention_mask = np.zeros(shape=[1, max_length], dtype=np.int16)
            label_ids = np.full(shape=[1, answer_length], fill_value=-100, dtype=np.int32)

            numeric_column_indexes = get_numeric_column(table_2d=table_data)
            if len(numeric_column_indexes) >= 2 and len(table_data) > 6 and check_table_length(
                    table_2d=table_data) is True:
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
                    return None

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

                for r, tr in enumerate(table_data):
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

                count = 0
                for j in range(length):
                    input_ids[count, j] = ids[j]
                    attention_mask[count, j] = 1

                inputs = tokenizer(answer_statement, return_tensors="np")
                ids = list(inputs['input_ids'][0, :])
                length = min(len(ids), answer_length)
                label_ids[count, 0: length] = ids[0: length]
                result.append((input_ids, attention_mask, label_ids))
        except:
            # check4 += 1
            continue

    if i % 1000 == 0:
        print(i)

    return result


if __name__ == "__main__":
    num_processes = 36  # 적절한 값을 설정하세요
    print(total_count)
    with Pool(processes=num_processes) as pool:
        # 작업을 병렬로 실행합니다.
        results = pool.map(process_data, range(3000))
    print('result:', len(results))
    total = 10
    for result in results:
        if result is None:
            continue

        print(len(result))
        total += len(result)

    print('total:', total)

    count = 0

    input_ids = np.zeros(shape=[total, max_length], dtype=np.int32)
    attention_mask = np.zeros(shape=[total, max_length], dtype=np.int16)
    label_ids = np.full(shape=[total, answer_length], fill_value=-100, dtype=np.int32)

    for result in results:
        if result is None:
            continue

        for res in result:
            input_ids, attention_mask, label_ids = res

            input_ids[count] = input_ids
            attention_mask[count] = attention_mask
            label_ids[count] = label_ids
            # print(tokenizer.decode(input_ids_[count, :256]))
            count += 1
    print('count:', count)

    np.save('input_ids_synthetic', input_ids[:count])
    np.save('attention_mask_synthetic', attention_mask[:count])
    np.save('label_ids_synthetic', label_ids[:count])





