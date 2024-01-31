import copy

import random

import template_config_simple as template_config
import table_utils
import operator

# from hierarchical_table_utils import make_hierarchical_table, make_hierarchical_structure


def weighted_randint(a, b):
    width = b - a

    accumulative_values = []
    for i, v in enumerate(list(reversed(range(1, width + 2)))):
        if i == 0:
            accumulative_values.append(v)
        else:
            accumulative_values.append(accumulative_values[-1] + v)
    r_idx = random.randint(0, accumulative_values[-1])

    for i in range(width + 1):
        if r_idx <= accumulative_values[i]:
            return i + a


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def division(a, b):
    return a / b


ops = {
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne
}


class ConditionObject:
    """
    random select
    random value
    random position
    random rank
    average
    median
    """
    def __init__(self, column_values, is_numeric_column, column_name, col_name_sep=False):
        if is_numeric_column is True:
            code_candidates = [0]
        else:
            code_candidates = [3]
        code_index = random.choice(code_candidates)

        self.object_value = 0
        self.object_name = ''

        self.column_name = str(column_name)
        if col_name_sep is True:
            self.column_name = '\'' + self.column_name + '\''

        if code_index == 0:
            # random select
            self.object_value = random.choice(column_values)
            self.object_name = str(self.object_value)
        if code_index == 1:
            # random value
            max_value = int(max(column_values))
            min_value = int(min(column_values))

            self.object_value = random.randint(min_value, max_value)
            self.object_name = str(self.object_value)
        if code_index == 2:
            # random position
            random_position = random.randint(0, len(column_values) - 1)
            self.object_value = column_values[random_position]

            random_position += 1
            object_name = random.choice(template_config.POSITION_EXPRESSION).replace('{pos}', str(random_position))
            self.object_name = object_name
        if code_index == 3:
            # random rank
            random_position = random.randint(0, len(column_values) - 1)
            arg_indices = list(reversed(table_utils.arg_sort(column_values)))

            rank_position = arg_indices[random_position]

            self.object_value = column_values[rank_position]

            random_position += 1
            object_name = random.choice(template_config.RANKING_EXPRESSION).replace('{pos}', str(random_position))
            self.object_name = object_name
        if code_index == 4:
            # average
            self.object_value = sum(column_values) / len(column_values)
            self.object_name = random.choice(template_config.AVERAGE_COL_EXPRESSION)
        if code_index == 5:
            # median
            self.object_value = table_utils.median(column_values)
            self.object_name = random.choice(template_config.MEDIAN_COL_EXPRESSION)
        self.object_name = self.object_name.replace('{column}', self.column_name)
        self.code_index = code_index


class ConditionStatement:
    """
    '{HIGHER_THAN}',
    '{HIGHER_THAN_EQUAL}',
    '{LOWER_THAN}',
    '{LOWER_THAN_EQUAL}',
    '{EQUAL}',
    '{NOT_EQUAL}',
]
    """
    def __init__(self,
                 table_2d,
                 column_candidates=None, col_name_sep=False):
        if column_candidates is None:
            column_candidates = list(range(len(table_2d[0])))

        select_column_index = random.choice(column_candidates)
        column_index = random.choice(column_candidates)

        self.result = True

        column_values = []
        for r in range(1, len(table_2d)):
            column_values.append(table_2d[r][column_index])
        is_numeric_column = table_utils.check_numeric_column(table_2d, column_index)
        self.condition_object = ConditionObject(column_values=column_values, is_numeric_column=is_numeric_column,
                                                column_name=table_2d[0][column_index])

        if is_numeric_column is True:
            code_candidates = [0]
        else:
            code_candidates = [4]
        code_index = random.choice(code_candidates)

        self.selected_rows = []
        self.selected_values = []
        self.selected_value_strings = []

        if code_index == 0:
            op_func = ops['<']
            self.condition_statement = random.choice(template_config.BIGGER_THAN_EXPRESSION)
        elif code_index == 1:
            op_func = ops['<=']
            self.condition_statement = random.choice(template_config.BIGGER_EQUAL_EXPRESSION)
        elif code_index == 2:
            op_func = ops['>']
            self.condition_statement = random.choice(template_config.LESS_THAN_EXPRESSION)
        elif code_index == 3:
            self.condition_statement = random.choice(template_config.LESS_EQUAL_EXPRESSION)
            op_func = ops['>=']
        elif code_index == 4:
            self.condition_statement = random.choice(template_config.EQUAL_EXPRESSION)
            op_func = ops['==']
        else:
            self.condition_statement = random.choice(template_config.NOT_EQUAL_EXPRESSION)
            op_func = ops['!=']
        self.condition_statement = self.condition_statement.replace('{column}', self.condition_object.column_name)
        self.condition_statement = self.condition_statement.replace('{object}', self.condition_object.object_name)

        for r, column_value in enumerate(column_values):
            if op_func(self.condition_object.object_value, column_value) is True:
                value = table_2d[r + 1][select_column_index]

                word = '[' + str(r) + ',' + str(select_column_index) + ']'
                self.selected_rows.append(word)
                self.selected_values.append(value)
                self.selected_value_strings.append(str(value))

        if len(self.selected_values) == 0:
            self.selected_values.append(-1)
            self.selected_value_strings.append('-1')
            self.result = False

        is_numeric_column = table_utils.check_numeric_column(table_2d, select_column_index)
        if is_numeric_column is True:
            code_candidates = [0]
        else:
            code_candidates = [3]
        code_index = random.choice(code_candidates)

        self.column_name = str(table_2d[0][select_column_index])
        if col_name_sep is True:
            self.column_name = '\'' + self.column_name + '\''

        self.statement_value = ''
        self.natural_statement = ''
        self.logic_statement_1 = ''
        self.logic_statement_2 = ''

        if code_index == 0:
            # sum
            self.statement_value = sum(self.selected_values)
            self.logic_statement_1 += '(' + ' + '.join(self.selected_value_strings) + ')'
            self.logic_statement_2 += '(' + ' + '.join(self.selected_rows) + ')'
            self.natural_statement = random.choice(template_config.SUM_COL_EXPRESSION)

        elif code_index == 1:
            # average
            self.statement_value = sum(self.selected_values) / len(self.selected_values)
            self.logic_statement_1 = '(' + ' + '.join(self.selected_value_strings) + ') / ' + str(len(self.selected_values))
            self.logic_statement_2 = '(' + ' + '.join(self.selected_rows) + ') / ' + str(len(self.selected_values))
            self.natural_statement = random.choice(template_config.AVERAGE_COL_EXPRESSION)

        elif code_index == 2:
            # median
            self.statement_value = table_utils.median(self.selected_values)
            self.logic_statement_1 = 'median(' + ', '.join(self.selected_value_strings) + ')'
            self.logic_statement_2 = 'median(' + ', '.join(self.selected_rows) + ')'
            self.natural_statement = random.choice(template_config.MEDIAN_COL_EXPRESSION)

        else:
            # count
            self.statement_value = len(self.selected_values)
            self.logic_statement_1 = 'count(' + ', '.join(self.selected_value_strings) + ')'
            self.logic_statement_2 = 'count(' + ', '.join(self.selected_rows) + ')'
            self.natural_statement = random.choice(template_config.COUNT_COL_EXPRESSION)

        self.natural_statement = self.natural_statement.replace('{column}', self.column_name)
        self.natural_statement += ' ' + self.condition_statement

        if code_index != 2 and code_index != 3:
            if len(self.selected_rows) == 1:
                self.logic_statement_1 = self.logic_statement_1.replace('(', '').replace(')', '')
                self.logic_statement_1 = self.logic_statement_1.replace(' / 1', '')


class Statement:
    def __init__(self,
                 table_2d,
                 input_condition_statement: ConditionStatement = None):
        self.result = True

        columns = []
        for c in range(len(table_2d[0])):
            column_values = []
            for r in range(1, len(table_2d)):
                if table_utils.check_numeric_column(table_2d, c) is True:
                    column_values.append(float(table_2d[r][c]))
                else:
                    column_values.append(table_2d[r][c])
            if table_utils.check_numeric_column(table_2d, c) is True:
                columns.append(column_values)
            else:
                columns.append(None)

        code_candidates = [0, 1, 2, 3, 4, 5, 6, 7]
        if input_condition_statement is not None:
            if input_condition_statement.statement_value > 500:
                code_candidates = [0, 1, 3, 4, 5, 6, 7]
        code_index = random.choice(code_candidates)

        code_index = 0
        column_candidates = []
        for c in range(len(table_2d[0])):
            column_candidates.append(c)
            if table_utils.check_numeric_column(table_2d=table_2d, column_index=c) is True:
                column_candidates.append(c)

        #self.statement_code = template_config.STATEMENTS[code_index]
        #self.statement_expression = ''

        if code_index < 4:
            object_num = 1
        elif code_index == 4 or code_index == 5 or code_index == 6:
            object_num = 2
        else:
            object_num = 2

        self.statement_objects = []
        for o in range(object_num):
            check = 0
            while True:
                check += 1
                if check >= 1000:
                    self.result = False
                    break

                # have to set how to create column indexes
                statement_object = ConditionStatement(table_2d, column_candidates)
                if statement_object.result is not False:
                    if code_index == 2 or code_index == 5:
                        if statement_object.statement_value > 500:
                            continue

                    if code_index == 3:
                        if statement_object.statement_value == 0:
                            continue

                    if code_index == 6 and o == 1:
                        if statement_object.statement_value == 0:
                            continue

                    self.statement_objects.append(statement_object)
                    break

        self.statement_value = 0
        self.statement_function = add
        self.natural_statement = ''
        self.logic_statement_1 = ''
        self.logic_statement_2 = ''

        input_statement = ''
        input_statement1 = ''
        input_statement2 = ''

        if self.result is False:
            code_index = 10

        # Sum Subtract Multiply Divide Add_Subtract Add_Multiply Add_Divide Add_Sum
        if code_index == 0:
            # Sum
            self.statement_value = self.statement_objects[0].statement_value
            self.logic_statement_1 = '+ ' + self.statement_objects[0].logic_statement_1
            self.logic_statement_2 = '+ ' + self.statement_objects[0].logic_statement_2
            self.natural_statement = random.choice(template_config.SUM_EXPRESSION)
            input_statement = self.statement_objects[0].natural_statement

        elif code_index == 1:
            # Subtract
            self.statement_value = -self.statement_objects[0].statement_value
            self.logic_statement_1 = '- ' + self.statement_objects[0].logic_statement_1
            self.logic_statement_2 = '- ' + self.statement_objects[0].logic_statement_2
            self.natural_statement = random.choice(template_config.SUBTRACT_EXPRESSION)
            input_statement = self.statement_objects[0].natural_statement

        elif code_index == 2:
            # Multiply
            self.statement_value = self.statement_objects[0].statement_value
            self.statement_function = multiply
            self.logic_statement_1 = '* ' + self.statement_objects[0].logic_statement_1
            self.logic_statement_2 = '* ' + self.statement_objects[0].logic_statement_2
            self.natural_statement = random.choice(template_config.MULTIPLY_EXPRESSION)
            input_statement = self.statement_objects[0].natural_statement

        elif code_index == 3:
            # Divide
            self.statement_value = self.statement_objects[0].statement_value
            self.statement_function = division
            self.logic_statement_1 = '/ ' + self.statement_objects[0].logic_statement_1
            self.logic_statement_2 = '/ ' + self.statement_objects[0].logic_statement_2
            self.natural_statement = random.choice(template_config.DIVIDE_EXPRESSION)
            input_statement = self.statement_objects[0].natural_statement

        elif code_index == 4:
            # Add Subtract
            self.statement_value = self.statement_objects[0].statement_value - self.statement_objects[1].statement_value
            self.logic_statement_1 = '+ (' + self.statement_objects[0].logic_statement_1
            self.logic_statement_1 += ' - ' + self.statement_objects[1].logic_statement_1 + ')'
            self.logic_statement_2 = '+ (' + self.statement_objects[0].logic_statement_2
            self.logic_statement_2 += ' - ' + self.statement_objects[1].logic_statement_2 + ')'
            self.natural_statement = random.choice(template_config.ADD_SUBTRACT_EXPRESSION)
            input_statement1 = self.statement_objects[0].natural_statement
            input_statement2 = self.statement_objects[1].natural_statement

        elif code_index == 5:
            # Add Multiply
            self.statement_value = self.statement_objects[0].statement_value * self.statement_objects[1].statement_value
            self.logic_statement_1 = '+ (' + self.statement_objects[0].logic_statement_1
            self.logic_statement_1 += ' * ' + self.statement_objects[1].logic_statement_1 + ')'
            self.logic_statement_2 = '+ (' + self.statement_objects[0].logic_statement_2
            self.logic_statement_2 += ' * ' + self.statement_objects[1].logic_statement_2 + ')'
            self.natural_statement = random.choice(template_config.ADD_MUL_EXPRESSION)
            input_statement = self.statement_objects[0].natural_statement + ' and '
            input_statement += self.statement_objects[1].natural_statement

        elif code_index == 6:
            # Add Divide
            self.statement_value = self.statement_objects[0].statement_value * self.statement_objects[1].statement_value
            self.logic_statement_1 = '+ (' + self.statement_objects[0].logic_statement_1
            self.logic_statement_1 += ' / ' + self.statement_objects[1].logic_statement_1 + ')'
            self.logic_statement_2 = '+ (' + self.statement_objects[0].logic_statement_2
            self.logic_statement_2 += ' / ' + self.statement_objects[1].logic_statement_2 + ')'
            self.natural_statement = random.choice(template_config.ADD_DIVIDE_EXPRESSION)
            input_statement1 = self.statement_objects[0].natural_statement
            input_statement2 = self.statement_objects[1].natural_statement
        elif code_index == 7:
            # Add SUM
            for o in range(object_num):
                self.statement_value += self.statement_objects[o].statement_value
                if o == 0:
                    self.logic_statement_1 += '+ (' + self.statement_objects[o].logic_statement_1
                    self.logic_statement_2 += '+ (' + self.statement_objects[o].logic_statement_2
                    input_statement = self.statement_objects[o].natural_statement
                else:
                    if o == object_num - 1:
                        input_statement += ' and ' + self.statement_objects[o].natural_statement
                    else:
                        input_statement += ', ' + self.statement_objects[o].natural_statement
                    self.logic_statement_1 += ' + ' + self.statement_objects[o].logic_statement_1
                    self.logic_statement_2 += ' + ' + self.statement_objects[o].logic_statement_2
            self.logic_statement_1 += ')'
            self.logic_statement_2 += ')'
            self.natural_statement = random.choice(template_config.ADD_SUM_EXPRESSION)

        self.natural_statement = self.natural_statement.replace('{input}', input_statement)
        self.natural_statement = self.natural_statement.replace('{input1}', input_statement1)
        self.natural_statement = self.natural_statement.replace('{input2}', input_statement2)

        # Sum Subtract Multiply Divide Add_Subtract Add_Multiply Add_Divide Add_Sum
        op_list = [
            'sum', 'subtract', 'multiply', 'divide', 'add subtract', 'add multiply',
            'add divide', 'add sum', '', '', '', '', ''
        ]
        self.operation_word = op_list[code_index]


class ExpressionObject:
    def __init__(self, table_2d):
        column_candidates = []
        for c in range(len(table_2d[0])):
            column_candidates.append(c)
            if table_utils.check_numeric_column(table_2d=table_2d, column_index=c) is True:
                column_candidates.append(c)

        while True:
            statement_object = ConditionStatement(table_2d, column_candidates)
            if statement_object.result is not False:
                break

        self.begin_statement = statement_object
        self.statements = []

        num_of_statement = weighted_randint(1, 3)
        for n in range(num_of_statement):
            while True:
                statement_object = Statement(table_2d, input_condition_statement=self.begin_statement)
                if statement_object.result is not False:
                    break
            self.statements.append(statement_object)

        self.natural_statement = random.choice(template_config.EXPRESSION_AT_START)
        self.natural_statement = self.natural_statement.replace('{STATEMENT}', self.begin_statement.natural_statement)
        self.logic_statement = self.begin_statement.logic_statement_1
        self.logic_statement_1 = self.begin_statement.logic_statement_1
        self.logic_statement_2 = self.begin_statement.logic_statement_2
        self.sentences = []

        for n in range(num_of_statement):
            self.logic_statement_1 += ' ' + self.statements[n].logic_statement_1
            self.logic_statement_2 += ' ' + self.statements[n].logic_statement_2
            if n == 0 and len(template_config.EXPRESSION_AT_START) > 1:
                self.natural_statement += ', and ' + self.statements[n].natural_statement
            else:
                self.natural_statement += '. And ' + self.statements[n].natural_statement
        self.natural_statement += '.'

    def check_position(self):
        check = False

        if self.begin_statement.condition_object.code_index == 2 or \
                self.begin_statement.condition_object.code_index == 3:
            check = True

        for statement_object in self.statements:
            for condition_object in statement_object.statement_objects:
                if condition_object.condition_object.code_index == 2 or \
                        condition_object.condition_object.code_index == 3:
                    check = True

        return check


def convert_data2sentence(columns, cells, column_labels):
    name_column = 0
    rank_text = ''
    date_text = ''

    rank_column = -1

    for c in range(len(column_labels)):
        if column_labels[c] == 2:
            rank_text = cells[c]
            rank_column = c

        if column_labels[c] == 0:
            name_column = c
            break

    is_person = table_utils.check_person_entity(columns[name_column])

    start_column = None
    base_columns = []

    for c in range(len(column_labels)):
        if c == name_column:
            continue

        if c == rank_column:
            continue

        if start_column is None:
            start_column = c
            continue

        base_columns.append(c)

    sentence = '{}\'s {} is {}. '.format(cells[name_column], columns[start_column], cells[start_column])
    if rank_text != '':
        rank_sentence = random.choice(template_config.NER_RANK_EXPRESSION).replace('{RANK}', rank_text)
        sentence = rank_sentence + sentence

    if date_text != '':
        sentence = sentence + '[SEP]'
        date_sentence = 'at {}'.format(date_text) + '.'
        sentence = sentence.replace('. [SEP]', date_sentence)

    if is_person is True:
        sentence += 'And his/her '
    else:
        sentence += 'And its '

    for b, c in enumerate(base_columns):
        if b == 0 and len(base_columns) == 1:
            sentence += '{} is {}.'.format(columns[c], cells[c])
        elif b < len(base_columns) - 1:
            sentence += '{} is {}, '.format(columns[c], cells[c])
        else:
            sentence += 'and {} is {}.'.format(columns[c], cells[c])

    return sentence


class RandomExpression:
    def __init__(self, table_2d):
        table_2d = copy.deepcopy(table_2d)

        self.task_type = random.choice(
            [0, 1]
        )
        self.rank_column = 0

        if table_utils.find_sequential_column(table_2d=table_2d) == -1:
            table_2d[0].insert(0, 'Pos')

            for r in range(1, len(table_2d)):
                table_2d[r].insert(0, str(r))
        else:
            self.rank_column = table_utils.find_sequential_column(table_2d=table_2d)
        numeric_columns = table_utils.get_numeric_column(table_2d=table_2d)

        # functions for notation expression
        funcs = [
            template_config.summation,
            template_config.average,
            template_config.median,
            template_config.biggest,
            template_config.smallest,
            template_config.growth_rate,
            template_config.multiply,
            template_config.division
        ]

        code_candidates = [0, 1, 2, 3, 4, 5, 6, 7]
        code_index = random.choice(code_candidates)

        selected_columns = []

        if 0 <= code_index <= 5:
            num_object = weighted_randint(2, 4)
        else:
            num_object = 2

        for c in range(num_object):
            if len(numeric_columns) >= num_object:
                while True:
                    selected_column = random.choice(numeric_columns)

                    if (selected_column in selected_columns) is False:
                        selected_columns.append(selected_column)
                        break
            else:
                selected_column = random.choice(numeric_columns)
                selected_columns.append(selected_column)

        selected_column_names = []
        for c in selected_columns:
            selected_column_names.append(
                table_2d[0][c]
            )
        self.selected_column_names = selected_column_names
        self.selected_columns = selected_columns

        input_word = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        logic_statement = ''

        # sum, average, median, biggest, smallest, Growth Rate (X-Y)/Y, Multiply(2), Division(2)
        if code_index == 0:
            logic_statement = ' + '.join(input_word[:num_object])
        elif code_index == 1:
            logic_statement = ' + '.join(input_word[:num_object]) + ' / ' + str(num_object)
        elif code_index == 2:
            logic_statement = 'median(' + ', '.join(input_word[:num_object]) + ')'
        elif code_index == 3:
            logic_statement = 'max(' + ', '.join(input_word[:num_object]) + ')'
        elif code_index == 4:
            logic_statement = 'min(' + ', '.join(input_word[:num_object]) + ')'
        elif code_index == 5:
            logic_statement = '({} - {}) / {}'.format('A', 'B', 'B')
        elif code_index == 6:
            logic_statement = 'A * B'
        elif code_index == 7:
            logic_statement = 'A / B'

        self.logic_statement = logic_statement

        self.new_column_head = '[generated]'
        condition = ', '.join(self.selected_column_names)

        if self.task_type == 0:
            self.query = 'If the columns selected to generate a new value for the [generated] column are {}, ' + \
                         'what is the formula expression for the new value?'.format(condition)
            self.answer_text = self.logic_statement
        else:
            self.query = 'If the formula expression to generate a new value for the [generated] column are {}, ' + \
                         'what is the selected columns for the new value?'.format(self.logic_statement)
            self.answer_text = condition

        new_columns = []
        table_2d[0].append(self.new_column_head)

        for r in range(1, len(table_2d)):
            values = []
            for c in selected_columns:
                values.append(table_2d[r][c])

            try:
                column_value = funcs[code_index](values)
            except:
                column_value = 'Nan'
            new_columns.append(column_value)
            table_2d[r].append(column_value)

        self.new_columns = new_columns

        # set table-to-text sentence
        column_labels = [0] * len(table_2d[0])
        for c in numeric_columns:
            column_labels[c] += 1
        column_labels[self.rank_column] = 2

        if len(table_2d) < 10:
            num_of_sentences = 1
        elif len(table_2d) < 15:
            num_of_sentences = weighted_randint(2, 4)
        elif len(table_2d) < 20:
            num_of_sentences = weighted_randint(3, 5)
        else:
            num_of_sentences = weighted_randint(3, 10)

        rows_to_text = []
        for r in range(num_of_sentences):
            r_idx = random.choice(
                list(range(1, len(table_2d)))
            )

            row = table_2d.pop(r_idx)
            rows_to_text.append(row)

        sentences = []
        for r in range(num_of_sentences):
            sentence = convert_data2sentence(
                columns=table_2d[0],
                cells=rows_to_text[r],
                column_labels=column_labels
            )
            sentences.append(sentence)

        self.sentences = sentences
        self.table_2d = table_2d


class RandomQueryExpression:
    def __init__(self, table_2d):
        table_2d = copy.deepcopy(table_2d)
        self.expression_object = ExpressionObject(table_2d=table_2d)

        self.logic_statement = self.expression_object.logic_statement_1
        self.natural_statement = self.expression_object.natural_statement

        self.rank_column = table_utils.find_sequential_column(table_2d)
        if self.expression_object.check_position() is True and self.rank_column == -1:
            self.rank_column = 0

            table_2d[0].insert(0, 'Pos')
            for r in range(1, len(table_2d)):
                table_2d[r].insert(0, str(r))

        # set table-to-text sentence
        numeric_columns = table_utils.get_numeric_column(table_2d=table_2d)

        column_labels = [0] * len(table_2d[0])
        for c in numeric_columns:
            column_labels[c] += 1
        column_labels[self.rank_column] = 2

        if len(table_2d) < 10:
            num_of_sentences = 1
        elif len(table_2d) < 15:
            num_of_sentences = weighted_randint(2, 4)
        elif len(table_2d) < 20:
            num_of_sentences = weighted_randint(3, 5)
        else:
            num_of_sentences = weighted_randint(3, 10)

        rows_to_text = []
        for r in range(num_of_sentences):
            r_idx = random.choice(
                list(range(1, len(table_2d)))
            )

            row = table_2d.pop(r_idx)
            rows_to_text.append(row)

        sentences = []
        for r in range(num_of_sentences):
            sentence = convert_data2sentence(
                columns=table_2d[0],
                cells=rows_to_text[r],
                column_labels=column_labels
            )
            sentences.append(sentence)

        self.sentences = sentences
        self.table_2d = table_2d


def permutate_logic(query: str):
    max_convert = weighted_randint(1, 4)
    count = 0
    tks = query.split('. And ')

    while count < max_convert:
        t = random.randint(0, len(tks) - 1)
        tk = tks[t]

        if count >= max_convert or random.random() > 0.5:
            continue
        else:
            count += 1

        if tk.find('-th positioned row\'s element') != -1:
            tk = tk.replace('-th positioned row\'s element', '-th biggest value')
            # print('11!')
        elif tk.find('-th biggest value') != -1:
            tk = tk.replace('-th biggest value', '-th positioned row\'s element')
            # print('10!')
        elif tk.find('average') != -1:
            # print('9!')
            tk = tk.replace('average', 'median')
        elif tk.find('median') != -1:
            # print('8!')
            tk = tk.replace('median', 'average')
        elif tk.find('is greater than or equal to') != -1:
            # print('7!')
            if random.random() > 0.5:
                tk = tk.replace('is greater than or equal to', 'is greater than')
            else:
                tk = tk.replace('is greater than or equal to', 'is less than or equal to')
        elif tk.find('is less than or equal to') != -1:
            # print('6!')
            if random.random() > 0.5:
                tk = tk.replace('is less than or equal to', 'is less than')
            else:
                tk = tk.replace('is less than or equal to', 'is less than or equal to')
        elif tk.find('is greater than') != -1:
            # print('5!')
            if random.random() > 0.5:
                tk = tk.replace('is greater than', 'is less than')
            else:
                tk = tk.replace('is greater than', 'is greater than or equal to')
        elif tk.find('is less than') != -1:
            # print('4!')
            if random.random() > 0.5:
                tk = tk.replace('is less than', 'is greater than')
            else:
                tk = tk.replace('is less than', 'is less than or equal to')
        elif tk.find('subtract') != -1:
            # print('3!')
            tk = tk.replace('subtract', 'add')
        elif tk.find('multiply by') != -1:
            # print('2!')
            tk = tk.replace('multiply by', 'divide by')
        elif tk.find('divide by') != -1:
            # print('1!')
            tk = tk.replace('divide by', 'multiply by')
        tks[t] = tk

    return '. And '.join(tks)

if __name__ == "__main__":
    age_column = ['age', 27, 29, 31, 35, 45, 23, 21]
    height_column = ['height', 167, 169, 151, 185, 186, 190, 143]
    weight_column = ['weight', 59, 63, 47, 86, 121, 88, 40]
    name_column = ['name', 'John', 'Janny', 'Robin', 'Ken', 'Kenny', 'Dan', 'Eric']

    table_2d = []
    for i in range(8):
        table_2d.append(
            [age_column[i], height_column[i], weight_column[i], name_column[i]]
        )

    for i in range(1000):
        rqe = ExpressionObject(table_2d=table_2d)
        print(rqe.natural_statement)
        print('-------------')


