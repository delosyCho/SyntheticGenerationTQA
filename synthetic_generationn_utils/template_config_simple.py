import numpy as np
import table_utils

BASE_OPERATIONS = [
    'SUM', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'ADD_SUBTRACT', 'ADD_DIVIDE', 'ADD_SUM', 'ADD_MULTIPLY'
]

STATEMENTS = [
    '{CONDITION_SELECTION}',
    '{SELECTION_HEAD_POSITION}',
    '{SELECTION_HEAD_RANKING}',
    '{MEDIAN}',
    '{MOST_FREQUENT}'
]

# input statement for condition statement
BASE_STATEMENTS = [
    '{SIMPLE_SELECTION}',
    '{AVERAGE}',
    '{MEDIAN}',
    '{MOST_FREQUENT}'
]

CONDITIONS = [
    '{HIGHER_THAN}',
    '{HIGHER_THAN_EQUAL}',
    '{LOWER_THAN}',
    '{LOWER_THAN_EQUAL}',
    # if condition head is not numeric
    '{EQUAL}',
    '{NOT_EQUAL}',
]

# Operations to make single value using condition results
CONDITION_OPERATIONS = [
    '{SUM}',
    '{AVERAGE}',
    '{MEDIAN}',
    '{COUNT}'
]

POSITION_EXPRESSION = [
    '{pos}-th positioned row\'s element',
]

RANKING_EXPRESSION = [
    '{pos}-th biggest value',
]

AVERAGE_EXPRESSION = [
    'average value',
]

MEDIAN_EXPRESSION = [
    'median value',
]

BIGGER_THAN_EXPRESSION = [
    "where {column} is greater than {object}",
]

BIGGER_EQUAL_EXPRESSION = [
    "where {column} is greater than or equal to {object}",
]

LESS_THAN_EXPRESSION = [
    "where {column} is less than {object}",
]

LESS_EQUAL_EXPRESSION = [
    "where {column} is less than or equal to {object}",
]

EQUAL_EXPRESSION = [
    "where {column} is equal to {object}",
]

NOT_EQUAL_EXPRESSION = [
    "where {column} is not equal to {object}",
]

SUM_COL_EXPRESSION = [
    "sum of {column}",
]

AVERAGE_COL_EXPRESSION = [
    'average {column} value',
]

MEDIAN_COL_EXPRESSION = [
    'median {column} value',
]

COUNT_COL_EXPRESSION = [
    "count number of {column}",
]


SUM_EXPRESSION = [
    "add {input}",
]


SUBTRACT_EXPRESSION = [
    "subtract {input}"
]


SUBTRACT_EXPRESSION_VALUE = [
    "subtraction value between {input}"
]


MULTIPLY_EXPRESSION = [
    "multiply by {input}",
]


DIVIDE_EXPRESSION = [
    "divide by {input}",
]


ADD_SUBTRACT_EXPRESSION = [
    "add the result of subtracting {input2} from {input1}",
]


ADD_DIVIDE_EXPRESSION = [
    "add the result of dividing {input1} by {input2}",
]


ADD_SUM_EXPRESSION = [
    "add the sum of {input}",
]

ADD_MUL_EXPRESSION = [
    "add the result of the multiplication of {input}",
]

EXPRESSION_AT_START = [
    'Find a {STATEMENT}',
]


NER_RANK_EXPRESSION = [
    'At position {RANK}, ',
]


COUNTRY_EXPRESSION = [
    'nation', 'state', 'country', 'origin', 'citizenship'
]


CITY_EXPRESSION = [
    'city', 'urban Area', 'district', 'township', 'town'
]

ID_EXPRESSION = [
    'ID', 'license number', 'card number', 'tag', 'certification code', 'code', 'security code'
]


YEAR_EXPRESSION = [
    'year', 'calender year', 'solar year'
]


MONTH_EXPRESSION = [
    'month', 'calendar month', 'solar month'
]


DEPARTMENT_EXPRESSION = [
    'department', 'division', 'office', 'unit', 'segment', 'branch', 'sector'
]


# sum, average, median, biggest, smallest, Growth Rate (X-Y)/Y, Ratio, Multiply(2), Division(2)
def summation(values):
    return sum(values)


def average(values):
    return sum(values) / len(values)


def median(values):
    return table_utils.median(values)


def biggest(values):
    return max(values)


def smallest(values):
    return min(values)


def growth_rate(values):
    return (values[0] - values[1]) / values[1]


def division(values):
    return values[0] / values[1]


def multiply(values):
    return values[0] * values[1]






