import openai


# 발급받은 API 키 설정
OPENAI_API_KEY = "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"

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"


def table_to_string(table_2d):
    table_text = '['

    for tr in table_2d:
        line = '['
        for td in tr:
            line += str(td) + ', '
        line = line.strip(', ') + ']'
        table_text += line + ', '
    table_text = table_text.strip(', ') + ']'
    return table_text



example_table_2d = [
    ['count', 'year', 'city', 'revenue'],
    ['2', '1978', 'London', '231,770'],
    ['2', '1982', 'Boston', '89,550'],
    ['2', '1972', 'Los Angeles.', '178,310'],
    ['2', '1990', 'New York', '1,570,340'],
    ['1', '1968', 'Beijing', '34,499'],
    ['1', '1974', 'Seoul', '67,860'],
    ['1', '1980', 'Tokyo', '121,570'],
]

example_statement = 'tabular input: ' + table_to_string(example_table_2d) + ' When input query is \"Of the events held before 1980, what was the total revenue from events held in Asian cities?\", '
example_statement += 'the answer should be generated is \"select year < \'1980\', select city == \'Tokyo\' or \'Beijing\' or \'Seoul\', return sum(revenue)'

example_statement += 'Here\'s another example. When input query is \"For events held since 1979 with a count of 2, name the U.S. city that hosted an event with revenue less than or equal to Tokyo.\", '
example_statement += 'the answer should be generated is \"select count == 1, select city == \'Boston\' or \'Los Angeles\' or \'New York\', select revenue >= row 7, select year < \'1979\', return select(city)\" '

example_statement += 'Here\'s another example. When input query is \"For a city with a count of 2, what is the difference between the value with the largest revenue and the smallest?\", '
example_statement += 'the answer should be generated is \"select count == 2, return max(revenue) - min(revenue)\" '

explanation_statement = '\'select\' operation selects data that meets condition. Condition operation list is [==, !=, <, <=, >, >=]'
explanation_statement += '\'return\' operation returns final answer. In return, [count, average, select] is used. Operation is used with header name like this \'average(age)\'. '
explanation_statement += 'And the arithmetic can be used in return operation like this \'average(height) - min(height)\' '
# explanation_statement += 'In some cases, semantic analysis is needed to select data such as \'US city\' and \'Asia city\'.'

# explanation_statement += 'You have to select data with row like \'row 1, 3, 5\'. '


def generate_answer(table_2d):
    table_text = table_to_string(table_2d=table_2d)

    # 질문 작성하기
    query = "When making QA dataset for tabular data, i want to create execution query that represents the process of getting an final answer." + example_statement + explanation_statement
    query += "Use the following tabular inputs, please generate a new question and its corresponding answer. Please generate multiple data sets of less than 10 using different operations. tabular input:"
    query += table_text + ' '

    # 메시지 설정하기
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']

    return answer


def convert_query(query_to_convert):
    # 질문 작성하기
    query = "Vary the input questions so that they have different vocabulary or sentence structures. Try not to " \
            f"change the logical structure of the question, so the output should be the same. input question: " \
            f"\"{query_to_convert}\""

    # 메시지 설정하기
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']

    return answer