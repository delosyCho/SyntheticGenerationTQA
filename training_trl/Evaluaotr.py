import torch
import numpy as np
from collections import OrderedDict

from transformers import AutoModelForSequenceClassification, AutoTokenizer


class Evaluator:
    def __init__(self, device=None):
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-large")
        self.model = AutoModelForSequenceClassification.from_pretrained("roberta-large")

        # flan-t5  query conversion
        loaded_state_dict = torch.load('roberta-large-evaluator')
        new_state_dict = OrderedDict()
        for n, v in loaded_state_dict.items():
            name = n.replace("module.", "")  # .module이 중간에 포함된 형태라면 (".module","")로 치환
            new_state_dict[name] = v
        self.model.load_state_dict(new_state_dict, strict=True)
        self.model.to(device)
        self.device = device

    def propagate(self, query1, query2):
        inputs = self.tokenizer(query1, query2, return_tensors="pt")
        if self.device:
            inputs = tuple(t.to(self.device) for t in inputs)

        with torch.no_grad():
            logits = self.model(**inputs).logits
        return (torch.softmax(logits, dim=-1)[:, 0].detach().cpu().numpy() - 0.5) * 2
