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
    '{pos}-th value',
    '{pos}-th element',
    'position {pos} value',
    'value at {pos}th position',
    'value in the {pos}the place',
    'value at index {pos}',
    'index at {pos}',
]

RANKING_EXPRESSION = [
    '{pos}-th largest value',
    '{pos}-th biggest value',
    '{pos}-th largest element',
    '{pos}-th biggest element',
    'value ranked in {pos}-th size',
    'element ranked in {pos}-th size',
]

AVERAGE_EXPRESSION = [
    'average value',
    'average amount',
    'mean value',
    'mean'
]

MEDIAN_EXPRESSION = [
    'median value',
    'central value',
    'midpoint number',
    'median',
    'mid-range value',
    'median amount',
    'median point'
]

BIGGER_THAN_EXPRESSION = [
    "where {column} is greater than {object}",
    "where {column} exceeds {object}",
    "where {column} is more than {object}",
    "where {column} surpasses {object}",
    "where {column} tops {object}",
    "where {column} is above {object}",
    "where {column} outnumbers {object}",
    "where {column} is higher than {object}",
    "where {column} overtakes {object}",
    "where {column} is in excess of {object}",
]

BIGGER_EQUAL_EXPRESSION = [
    "where {column} is greater than or equal to {object}",
    "where {column} is not less than {object}",
    "where {column} is at least {object}",
    "where {column} exceeds or equals {object}",
    "where {column} is more than or equal to {object}",
    "where {column} is equal to or surpasses {object}",
    "where {column} is above or equal to {object}",
    "where {column} is higher than or the same as {object}"
]

LESS_THAN_EXPRESSION = [
    "where {column} is less than {object}",
    "where {column} is smaller than {object}",
    "where {column} is fewer than {object}",
    "where {column} is beneath {object}",
    "where {column} is lower than {object}",
    "where {column} is under {object}",
    "where {column} falls short of {object}",
    "where {column} is not as much as {object}",
    "where {column} is inferior to {object}",
    "where {column} lags behind {object}"
]

LESS_EQUAL_EXPRESSION = [
    "where {column} is less than or equal to {object}",
    "where {column} is not greater than {object}",
    "where {column} is at most {object}",
    "where {column} is equal to or less than {object}",
    "where {column} is no more than {object}",
    "where {column} is below or equal to {object}",
    "where {column} is up to {object}",
    "where {column} is lower than or equal to {object}"
]

EQUAL_EXPRESSION = [
    "where {column} is equal to {object}",
    "where {column} equals {object}",
    "where {column} is identical to {object}",
    "where {column} matches {object}",
    "where {column} corresponds to {object}",
    "where {column} is the same as {object}",
    "where {column} is equivalent to {object}"
]

NOT_EQUAL_EXPRESSION = [
    "where {column} is not equal to {object}",
    "where {column} does not equal {object}",
    "where {column} is different from {object}",
    "where {column} is not the same as {object}",
    "where {column} doesn't match {object}",
    "where {column} is unequal to {object}",
    "where {column} varies from {object}",
    "where {column} is dissimilar to {object}"
]

SUM_COL_EXPRESSION = [
    "sum of {column}",
    "total of {column}",
    "aggregate of {column}",
    "total sum of {column}",
    "combined total of {column}",
    "accumulated sum of {column}",
    "overall sum of {column}"
]

AVERAGE_COL_EXPRESSION = [
    'average {column} value',
    'average {column} amount',
    'average of {column}',
    'mean {column} value',
    'mean {column}'
]

MEDIAN_COL_EXPRESSION = [
    'median {column} value',
    'central {column} value',
    'midpoint number of {column}',
    'median of {column}',
    'mid-range value of {column}',
    'median amount of {column}',
    'median point of {column}'
]

COUNT_COL_EXPRESSION = [
    "count number of {column}",
    "tally of {column}",
    "total count of {column}",
    "number of {column} entries",
    "quantity of {column}",
    "sum of {column} instances",
    "count of {column} records",
    "total instances of {column}",
]


SUM_EXPRESSION = [
    "add {input}",
    "include {input}",
    "sum up with {input}",
    "combine with {input}",
    "incorporate {input}",
    "plus {input}"
]


SUBTRACT_EXPRESSION = [
    "subtract {input}"
    "deduct {input}",
    "exclude {input}",
    "take away {input}",
    "minus {input}"
]


SUBTRACT_EXPRESSION_VALUE = [
    "subtraction value between {input}"
    "deduction between {input}",
    "excluded value between {input}",
    "minus value between {input}"
]


MULTIPLY_EXPRESSION = [
    "multiply by {input}",
    "times {input}",
    "scale by {input}",
    "factor in {input}",
    "amplify by {input}",
    "multiply with {input}"
]


DIVIDE_EXPRESSION = [
    "divide by {input}",
    "divide through by {input}",
    "divide across {input}",
    "divide evenly by {input}",
    "partition by {input}",
    "segment by {input}"
]


ADD_SUBTRACT_EXPRESSION = [
    "add the result of subtracting {input2} from {input1}",
    "include the difference between {input1} and {input2}",
    "sum up the value obtained by subtracting {input2} from {input1}",
    "combine the outcome of {input1} minus {input2}",
    "incorporate the subtraction result of {input1} and {input2}",
    "add together the difference of {input1} and {input2}",
    "add the value of {input1} less {input2}"
]


ADD_DIVIDE_EXPRESSION = [
    "add the result of dividing {input1} by {input2}",
    "include the quotient of {input1} divided by {input2}",
    "sum up the value obtained by dividing {input1} by {input2}",
    "combine the outcome of {input1} divided by {input2}",
    "incorporate the division result of {input1} over {input2}",
    "add together the quotient of {input1} and {input2}",
    "add the value of {input1} divided by {input2}"
]


ADD_SUM_EXPRESSION = [
    "add the sum of {input}",
    "include the total of {input}",
    "add together the sum of {input}",
    "combine the sum of {input}",
    "incorporate the aggregate of {input}",
    "sum up {input} and add it",
    "add the result of summing {input}"
]

ADD_MUL_EXPRESSION = [
    "add the product of {input}",
    "sum up the multiplied value of {input}",
    "combine the result of multiplying {input}",
    "add together the multiplication of {input}",
    "include the product of multiplying {input}",
    "add the result of the multiplication of {input}",
    "incorporate the multiplied outcome of {input}"
]

EXPRESSION_AT_START = [
    'There is a value which is the {STATEMENT}',
    'On {STATEMENT}',
    'With {STATEMENT}',
    'Append to {STATEMENT}',
    'Put on top of {STATEMENT}'
]


NER_RANK_EXPRESSION = [
    'At position {RANK}, ',
    'With a position of {RANK}, ',
    'With pos {RANK}, ',
    'Positioned {RANK}, '
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






