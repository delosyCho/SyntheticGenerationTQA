import random
import string

import template_config
# import synthesize_utils
# from synthesize_utils import Statement
from synthesize_utils import *

class HierarchicalStructure:
    def __init__(self, rows_for_parent, rows_for_node, parent2node,
                 parent_table_2d, node_table_2d, new_table_2d, table_2d, parent_type, node_type):
        self.rows_for_parent = rows_for_parent
        self.rows_for_node = rows_for_node
        self.parent2node = parent2node
        self.parent_table_2d = parent_table_2d
        self.node_table_2d = node_table_2d
        self.new_table_2d = new_table_2d
        self.table_2d = table_2d

        self.parent_type = parent_type
        self.node_type = node_type

    def generate_hierarchical_statement(self, input_condition_statement):
        parent_statement = ''
        node_statement = ''

        if len(self.rows_for_parent) > 0:
            nodes = []

            column_index = random.randint(1, len(self.table_2d[0]) - 1)

            # code
            # equal, not equal, max, min, bigger, lower, position
            code_index = random.randint(0, 4)

            values = [0]
            for i in range(1, len(self.parent_table_2d)):
                values.append(self.parent_table_2d[i][column_index])

            if code_index == 0 or code_index == 1:
                code_index = 1
                # equal
                r_idx = random.randint(1, len(self.parent_table_2d))
                value = self.parent_table_2d[r_idx][column_index]

                for i in range(1, len(self.parent_table_2d)):
                    if code_index == 0:
                        if value == values[i]:
                            nodes.extend(self.parent2node[i - 1])
                    else:
                        if value != values[i]:
                            nodes.extend(self.parent2node[i - 1])

                if code_index == 0:
                    parent_statement += str(random.choice(template_config.EQUAL_EXPRESSION)).replace('where ', '')
                else:
                    parent_statement += str(random.choice(template_config.NOT_EQUAL_EXPRESSION)).replace('where ', '')
                parent_statement = parent_statement.replace('{column}', self.parent_table_2d[0][column_index])
                parent_statement = parent_statement.replace('{object}', str(value))
            if code_index == 2 or code_index == 3:
                # bigger lower
                if random.randint(0, 1) == 0:
                    value = sum(values[1:]) / (len(values) - 1)
                else:
                    value = random.randint(min(values[1:]) * 100, max(values[1:]) * 100) / 100

                for i in range(1, len(self.parent_table_2d)):
                    if code_index == 4:
                        if values[i] > value:
                            nodes.extend(self.parent2node[i - 1])
                    else:
                        if values[i] < value:
                            nodes.extend(self.parent2node[i - 1])

                if code_index == 0:
                    parent_statement += str(random.choice(template_config.BIGGER_THAN_EXPRESSION)).replace('where ', '')
                else:
                    parent_statement += str(random.choice(template_config.LESS_THAN_EXPRESSION)).replace('where ', '')
                parent_statement = parent_statement.replace('{column}', self.parent_table_2d[0][column_index])
                parent_statement = parent_statement.replace('{object}', str(value))

            if code_index == 4:
                r_idx = random.randint(1, len(self.parent_table_2d) - 1)
                nodes.extend(self.parent2node[r_idx - 1])

                parent_statement += str(random.choice(template_config.POSITION_EXPRESSION)).replace('where ', '')
                parent_statement = parent_statement.replace('{pos}', str(r_idx))
                # parent_statement = parent_statement.replace('{pos}', str(r_idx))

        else:
            nodes = list(range(len(self.node_table_2d) - 1))

        node_table_2d = [self.node_table_2d[0]]
        for node in nodes:
            node_table_2d.append(self.node_table_2d[node + 1])

        new_table_2d = [self.table_2d[0]]
        rows = []

        column_index = random.randint(1, len(self.table_2d[0]) - 1)

        # code
        if len(self.rows_for_parent) > 0:
            code_index = random.randint(0, 3)
        else:
            code_index = random.randint(0, 4)

        values = [0]
        for i in range(1, len(self.node_table_2d)):
            # print(len(self.node_table_2d), i, column_index)
            values.append(self.node_table_2d[i][column_index])

        if code_index == 0 or code_index == 1:
            code_index = 1
            r_idx = random.randint(1, len(node_table_2d) - 1)
            value = node_table_2d[r_idx][column_index]

            for i in nodes:
                i = i + 1

                if code_index == 0:
                    if values[i] == values[r_idx]:
                        rows.extend(self.rows_for_node[i - 1])
                else:
                    if values[i] != values[r_idx]:
                        rows.extend(self.rows_for_node[i - 1])

            if code_index == 0:
                node_statement += str(random.choice(template_config.EQUAL_EXPRESSION)).replace('where ', '')
            else:
                node_statement += str(random.choice(template_config.NOT_EQUAL_EXPRESSION)).replace('where ', '')
            node_statement = node_statement.replace('{column}', self.node_table_2d[0][column_index])
            node_statement = node_statement.replace('{object}', str(value))
        if code_index == 2 or code_index == 3:
            # bigger lower
            if random.randint(0, 1) == 0:
                value = sum(values[1:]) / (len(values) - 1)
            else:
                value = random.randint(min(values[1:]) * 100, max(values[1:]) * 100) / 100

            for i in nodes:
                i = i + 1
                if code_index == 4:
                    if values[i] > value:
                        rows.extend(self.rows_for_node[i - 1])
                else:
                    if values[i] < value:
                        rows.extend(self.rows_for_node[i - 1])

            if code_index == 0:
                node_statement += str(random.choice(template_config.BIGGER_THAN_EXPRESSION)).replace('where ', '')
            else:
                node_statement += str(random.choice(template_config.LESS_THAN_EXPRESSION)).replace('where ', '')
            node_statement = node_statement.replace('{column}', self.node_table_2d[0][column_index])
            node_statement = node_statement.replace('{object}', str(value))

        if code_index == 4:
            r_idx = random.randint(1, len(self.node_table_2d) - 1)
            rows.extend(self.rows_for_node[r_idx - 1])

            node_statement += str(random.choice(template_config.POSITION_EXPRESSION)).replace('where ', '')
            node_statement = node_statement.replace('{pos}', str(r_idx))

        for r in rows:
            new_table_2d.append(self.table_2d[r])

        statement = Statement(table_2d=new_table_2d, input_condition_statement=input_condition_statement)

        type_config_list = [template_config.COUNTRY_EXPRESSION, template_config.CITY_EXPRESSION,
                            template_config.DEPARTMENT_EXPRESSION, template_config.ID_EXPRESSION,
                            template_config.YEAR_EXPRESSION, template_config.MONTH_EXPRESSION]

        # print(type_config_list[self.node_type])
        if len(parent_statement) > 2:
            word = random.choice(
                type_config_list[self.parent_type]
            )
            parent_statement = ' and within the ' + word + ' ' + parent_statement
            statement.natural_statement += parent_statement

        word = random.choice(
            type_config_list[self.node_type]
        )
        node_statement = ' and within the ' + word + ' ' + node_statement
        statement.natural_statement += node_statement

        return statement


class HierarchicalExpressionObject:
    def __init__(self, table_2d):
        table_2d = copy.deepcopy(table_2d)

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

        table_2d = copy.deepcopy(table_2d)
        hs = make_hierarchical_table(table_2d=table_2d)

        num_of_statement = weighted_randint(1, 3)
        for n in range(num_of_statement):
            while True:
                statement_object = hs.generate_hierarchical_statement(input_condition_statement=self.begin_statement)
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
            # self.logic_statement_2 += ' ' + self.statements[n].logic_statement_2
            if n == 0:
                self.natural_statement += ', and ' + self.statements[n].natural_statement
            else:
                self.natural_statement += '. And ' + self.statements[n].natural_statement
        self.natural_statement += '.'

        self.new_table_2d = copy.deepcopy(hs.new_table_2d)

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



def choose_random_department(count):
    departments = [
        "Sales", "Marketing", "Finance", "Human Resources", "Research and Development",
        "Customer Support", "IT", "Operations", "Production", "Quality Assurance",
        "Legal", "Public Relations", "Administration", "Purchasing", "Engineering",
        "Product Management", "Supply Chain", "Design", "Logistics", "Training",
        "Accounting", "Business Development", "Compliance", "Strategic Planning", "Health and Safety",
        "Project Management", "Internal Audit", "Corporate Communications", "Facilities", "Security",
        "Media Relations", "Brand Management", "Vendor Relations", "Event Planning", "Investor Relations",
        "Sustainability", "Community Outreach", "Sales Operations", "Merchandising", "Education",
        # 추가 부서를 이어서 나열하세요.
    ]

    # 랜덤하게 부서 선택
    selected_department = random.sample(departments, k=count)

    return selected_department


def generate_random_months(count):
    if count <= 0:
        return []

    start = random.randint(0, 12 - count)

    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    random_months = []
    for k in range(count):
        random_months.append(months[k + start])

    return random_months


def generate_random_years(count):
    start_year = random.randint(1980, 2020)
    if count <= 0:
        return []

    years = []
    for i in range(count):
        years.append(start_year)
        start_year += 1

    return years


def choose_random_city(count):
    cities = [
        "Seoul", "Tokyo", "Busan", "New York", "Los Angeles",
        "London", "Paris", "Beijing", "Sydney", "Toronto",
        "Chicago", "Berlin", "Rome", "Hong Kong", "Mumbai",
        "Shanghai", "Dubai", "San Francisco", "Amsterdam", "Singapore",
        "Miami", "Madrid", "Barcelona", "Bangkok", "Vienna",
        "Istanbul", "Rio de Janeiro", "Cape Town", "Toronto", "Vancouver",
        "Munich", "Zurich", "Osaka", "Seville", "Stockholm",
        "Budapest", "Prague", "Warsaw", "Dublin", "Edinburgh",
        # 추가 도시를 이어서 나열하세요.
    ]

    # 랜덤하게 도시 선택
    selected_city = random.sample(cities, k=count)

    return selected_city


def choose_random_country(count):
    countries = [
        "United States", "Canada", "United Kingdom", "France", "Japan",
        "China", "Germany", "Italy", "Spain", "Australia",
        "Brazil", "Argentina", "Russia", "India", "South Korea",
        "Mexico", "Netherlands", "Belgium", "Switzerland", "Sweden",
        "Norway", "Denmark", "Finland", "Portugal", "Greece",
        "Turkey", "Egypt", "South Africa", "New Zealand", "Singapore",
        # 추가 국가를 이어서 나열하세요.
    ]

    # 랜덤하게 국가 선택
    selected_country = random.sample(countries, k=count)

    return selected_country


def generate_id():
    # 알파벳 랜덤 선택 (예: A부터 Z까지)
    # alphabet = random.choice(string.ascii_uppercase)

    # 코드명 생성 (예: 0부터 9까지의 숫자로 이루어진 세 자리 문자열)
    s_length = random.randint(1, 3)
    n_length = random.randint(2, 5)

    symbols = ['', '', '-', '-', '#', '*']
    symbol_word = random.choice(symbols)

    alphabet = ''.join(random.choices(string.ascii_uppercase, k=s_length))
    code_name = ''.join(random.choices(string.digits, k=n_length))

    # 알파벳과 코드명을 결합하여 문자열 생성
    random_string = f"{alphabet}{symbol_word}{code_name}"

    return random_string


def generate_ids(count):
    generated_ids = []
    for _ in range(count):
        generated_ids.append(generate_id())
    return generated_ids


def parse_number(word):
    try:
        return float(word)
    except:
        return 0


def make_hierarchical_structure(row_len):
    num_of_node = random.randint(2, row_len // 2 + 1)

    node_list = [1] * num_of_node

    num_to_add = row_len - sum(node_list)
    for _ in range(num_to_add):
        idx = random.randint(0, num_of_node - 1)
        node_list[idx] += 1
    parent_of_node_list = []
    if num_of_node > 3:
        num_of_parent = random.randint(2, num_of_node // 2 + 1)
        parent_of_node_list = [1] * num_of_parent

        num_to_add = num_of_node - sum(parent_of_node_list)

        for _ in range(num_to_add):
            idx = random.randint(0, num_of_parent - 1)
            parent_of_node_list[idx] += 1

    return node_list, parent_of_node_list


def make_hierarchical_table(table_2d):
    funcs = [
        choose_random_country, choose_random_city, choose_random_department, generate_ids, generate_random_years, generate_random_months
    ]

    node_list, parent_of_node_list = make_hierarchical_structure(len(table_2d) - 1)
    # print(len(table_2d), len(table_2d[0]))
    # print(node_list)
    # print(parent_of_node_list)
    rows_for_node = []
    for i in range(len(node_list)):
        row_list = []

        b_ix = sum(node_list[:i])
        for j in range(b_ix, b_ix + node_list[i]):
            row_list.append(j + 1)
        rows_for_node.append(row_list)

    rows_for_parent = []
    for i in range(len(parent_of_node_list)):
        row_list = []

        b_ix = sum(parent_of_node_list[:i])
        for j in range(b_ix, b_ix + parent_of_node_list[i]):
            row_list.extend(rows_for_node[j])

        rows_for_parent.append(row_list)

    new_table_2d = [table_2d[0]]
    p_table_2d = [table_2d[0]]
    n_table_2d = [table_2d[0]]

    parent_type = -1
    node_type = -1

    if len(rows_for_parent) > 0:
        idx = random.randint(0, len(funcs) - 1)
        func1 = funcs[idx]
        parent_words = func1(count=len(rows_for_parent))
        parent_type = idx

        while True:
            idx = random.randint(0, len(funcs) - 1)
            func2 = funcs[idx]
            if func1 != func2:
                break
        node_words = func2(count=len(rows_for_node))
        node_type = idx

        for i in range(len(rows_for_parent)):
            row = []
            row.append(parent_words[i])
            for c in range(1, len(table_2d[0])):
                row.append(0)

            for r in rows_for_parent[i]:
                for c in range(1, len(table_2d[0])):
                    row[c] += parse_number(table_2d[r][c])
            new_table_2d.append(row)
            p_table_2d.append(row)

            for j in range(parent_of_node_list[i]):
                j = sum(parent_of_node_list[:i]) + j
                row = []
                row.append(node_words[j])
                for c in range(1, len(table_2d[0])):
                    row.append(0)

                for r in rows_for_node[j]:
                    for c in range(1, len(table_2d[0])):
                        row[c] += parse_number(table_2d[r][c])
                new_table_2d.append(row)
                n_table_2d.append(row)

                for r in rows_for_node[j]:
                    new_table_2d.append(table_2d[r])
    else:
        idx = random.randint(0, len(funcs) - 1)
        func = funcs[idx]
        node_words = func(count=len(rows_for_node))

        for j in range(len(rows_for_node)):
            row = []
            row.append(node_words[j])
            for c in range(1, len(table_2d[0])):
                row.append(0)

            for r in rows_for_node[j]:
                for c in range(1, len(table_2d[0])):
                    row[c] += parse_number(table_2d[r][c])
            new_table_2d.append(list(row))
            n_table_2d.append(row)

            for r in rows_for_node[j]:
                new_table_2d.append(table_2d[r])

    parent2node = []
    for p in range(len(parent_of_node_list)):
        nodes = []
        for j in range(parent_of_node_list[p]):
            b_idx = sum(parent_of_node_list[:p])
            nodes.append(
                b_idx + j
            )
        parent2node.append(nodes)

    hs = HierarchicalStructure(
        rows_for_parent=rows_for_parent,
        rows_for_node=rows_for_node,
        table_2d=table_2d,
        new_table_2d=new_table_2d,
        node_table_2d=n_table_2d,
        parent_table_2d=p_table_2d,
        parent2node=parent2node[:],
        parent_type=parent_type,
        node_type=node_type
    )

    return hs


if __name__ == "__main__":
    table_2d = [['A', 'B', 'C']]
    for n in range(10):
        table_2d.append(['a', n % 2, n // 2, n])

    hs = make_hierarchical_table(table_2d=table_2d)
    hs.generate_hierarchical_statement()

    print()