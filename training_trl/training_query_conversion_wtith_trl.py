import torch

from trl import PPOConfig, PPOTrainer, AutoModelForSeq2SeqLMWithValueHead, create_reference_model
from transformers import AutoTokenizer, T5ForConditionalGeneration

from collections import OrderedDict

from Reward_Utils import RewardUtil
import DataHolderTRL

batch_size = 32
config = PPOConfig(model_name="google/flan-t5-base", learning_rate=1e-7, batch_size=batch_size)

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

model = T5ForConditionalGeneration.from_pretrained('google/flan-t5-base')
loaded_state_dict = torch.load('flan-t5_query_conversion')
new_state_dict = OrderedDict()
for n, v in loaded_state_dict.items():
    name = n.replace("module.", "")  # .module이 중간에 포함된 형태라면 (".module","")로 치환
    new_state_dict[name] = v
model.load_state_dict(new_state_dict, strict=True)

model = AutoModelForSeq2SeqLMWithValueHead.from_pretrained(model)

ppo_trainer = PPOTrainer(
    model=model,
    config=config,
    tokenizer=tokenizer,
)
device = ppo_trainer.accelerator.device

generation_kwargs = {
    "max_length": 128,
    "min_length": -1,
    "top_k": 3,
    "top_p": 1.0,
    "do_sample": True,
    "pad_token_id": tokenizer.eos_token_id,
}

data_holder = DataHolderTRL.DataHolderTRL()
data_holder.batch_size = batch_size

num_of_epochs = 10
num_of_step = data_holder.input_ids.shape[0] // batch_size

reward_model = RewardUtil()

for epoch in range(num_of_epochs):
    for _ in range(num_of_step):
        input_ids, attention_mask = data_holder.next_batch()

        batch = {}

        input_ids_list = []
        for i in range(data_holder.batch_size):
            input_ids_list.append(input_ids[i])

        #### Get response from SFTModel
        response_tensors = ppo_trainer.generate(input_ids_list, **generation_kwargs)
        print(response_tensors[0].shape, response_tensors[1].shape)
        queries = tokenizer.batch_decode(input_ids, skip_special_tokens=True)
        responses = tokenizer.batch_decode(response_tensors, skip_special_tokens=True)

        #### Compute reward score
        rewards = []
        response_tensor_list = []

        for i in range(batch_size):
            reward_value = reward_model.get_reward(query1=queries[i], query2=responses[i])
            rewards.append(torch.FloatTensor([float(reward_value)]))
            response_tensor_list.append(response_tensors[i])
        # rewards = torch.FloatTensor(rewards)
        #### Run PPO step
        # Run PPO step
        _ = ppo_trainer.step(input_ids_list, response_tensor_list, rewards)
        print(epoch, rewards)

#### Save model
ppo_trainer.save_pretrained("my_ppo_model")