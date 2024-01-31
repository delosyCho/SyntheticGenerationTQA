import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time


# model_name = 'Upstage/SOLAR-10.7B-Instruct-v1.0'
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
)

input_query = "Find a midpoint number of weight where height doesn't match 179. And add the product of tally of age where age is at most 5-th biggest value and median of height where age is identical to value at 3th position. And plus median of height where height is lower than 175."
output = "median(weight where height != 179) +  rank("

# prompt_text = '[INST] ' + "Vary the input questions so that they have different vocabulary or sentence structures. " \
#               "Try not to change the logical structure of the question, so the output should be the same. " \
#               f"input question: {input_query} output: {output}" + ' [/INST]'

prompt_text = "Vary the input question so that they have different vocabulary or sentence structures. " \
              "Try not to change the logical structure of the question, so the output should be the same. " \
              "Generate only one question. " \
              f"input question: {input_query}"

conversation = [ {'role': 'user', 'content': prompt_text} ]

prompt = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)


from api_utils import convert_query
file = open('synthetic_queries3.txt', 'r', encoding='utf-8')
new_file = open('converted_synthetic_quries_mistral2_ver2.txt', 'w', encoding='utf-8')
lines = file.read().split('\n')

count = 0
# 시작 시간 기록
start_time = time.time()

for line in lines[30000:36000]:
    print(count)
    count += 1

    tks = line.split('\t')
    query1 = tks[0]
    query2 = tks[1]
    if query1 == query2:
        continue

    prompt_text = "Vary the input question so that they have different vocabulary or sentence structures. " \
                  "Numeric values and logical meaning must not be changed. " \
                  "Generate only one question. " \
                  f"input question: {query1}"

    conversation = [{'role': 'user', 'content': prompt_text}]
    prompt = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, use_cache=True, max_length=512)
    output_text1 = tokenizer.decode(outputs[0]).split('[/INST] ')[1]

    prompt_text = "Generate only one variation of the input question so that they have different vocabulary or sentence structures. " \
                  "Numeric values and logical meaning must not be changed. " \
                  "In particular, operations should be unchanged and clearly labeled. " \
                  f"input question: {query2}"

    conversation = [{'role': 'user', 'content': prompt_text}]
    prompt = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, use_cache=True, max_length=512)
    output_text2 = tokenizer.decode(outputs[0]).split('[/INST] ')[1]
    new_file.write(query1 + '\t' + query2 + '\t' + output_text1 + '\t' + output_text2 + '\n\t\n')

    print(query1, '====>>>>', output_text1)
    print()
    print(query2, '====>>>>', output_text2)
    print('-------------------------------------------------\n\n\n')

end_time = time.time()

# 소요된 시간 계산
elapsed_time = end_time - start_time

print(f"소요된 시간: {elapsed_time} 초")