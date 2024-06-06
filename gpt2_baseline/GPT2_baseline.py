# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import chardet
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
filepath = '/Users/CS224N/nytcrosswords.csv'
filepath = 'nytcrosswords.csv'
with open(filepath, 'rb') as file:
    result = chardet.detect(file.read())
    encoding = result['encoding']

df = pd.read_csv(filepath, encoding=encoding)
print(df.head())

relevant_cols = ['Clue', 'Word']
for col in relevant_cols:
    text_data = df[col].apply(str).tolist()
    training_text = "\n".join(text_data)


with open('training_data.txt', 'w', encoding='utf-8') as file:
    file.write(training_text)

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

tokenizer.pad_token = tokenizer.eos_token
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path='training_data.txt',
    block_size=128
)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

from transformers import pipeline

generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# text generation
text_prompt = ""
generated_text = generator(text_prompt, max_length=100, num_return_sequences=1)
print(generated_text[0]['generated_text'])

def answer_crossword(clue, length):
    prompt = f"Length of the word is: {length} Clue: {clue} Answer:"

    # Use the generator to generate text. Adjust max_length based on expected answer length
    response = generator(prompt, max_length=50, num_return_sequences=1)
    full_response = response[0]['generated_text']
    answer = full_response.split("Answer:")[1].strip().split('\n')[0].strip()

    return answer

answer_crossword('Harris in the Country Music Hall of Fame', 7)
