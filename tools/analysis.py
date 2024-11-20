import logging
from typing import List
from transformers import pipeline

logging.info("loading text-classification models...")
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None, max_length=512)

# sentences = ["I slept pretty good, but not long enough. I woke up with my shark still between my legs. which was a surprise! that means I probably didn't sleep on my belly."]
# model_outputs = classifier(sentences)
# print("-"*50)
# print(model_outputs[0])

def text_to_emotions(sentence: str):
    """
    TODO: write this docstring
    """
    model_outputs = classifier(sentence)[0]
    results = sorted(model_outputs, key=lambda x: x['score'], reverse=True)
    return results