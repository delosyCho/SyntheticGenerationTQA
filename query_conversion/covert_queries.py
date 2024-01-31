from api_utils import convert_query
file = open('synthetic_queries3.txt', 'r', encoding='utf-8')
new_file = open('converted_synthetic_quries_ver2.txt', 'w', encoding='utf-8')
lines = file.read().split('\n')

count = 0
for line in lines[0:30000]:
    print(count)
    count += 1

    tks = line.split('\t')
    query1 = tks[0]
    query2 = tks[1]
    if query1 == query2:
        continue

    while True:
        try:
            converted_query1 = convert_query(query1)
            converted_query2 = convert_query(query2)
            break
        except:
            continue

    new_file.write(query1 + '\t' + query2 + '\t' + converted_query1 + '\t' + converted_query2 + '\n\t\n')
    if count == 15000:
        break
new_file.close()