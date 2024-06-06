# -*- coding: utf-8 -*-
# this is a colab file so delete pips if running on IDE
!pip install accelerate
!pip install chardet

import pandas as pd
import numpy as np
import accelerate
import chardet
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

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

training_args = TrainingArguments(
    output_dir='./results',           
    overwrite_output_dir=True,       
    num_train_epochs=3,               
    per_device_train_batch_size=4,    
    save_steps=10_000,                
    save_total_limit=2,               
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

trainer.train()

from transformers import pipeline

model.save_pretrained('./my_finetuned_model')
tokenizer.save_pretrained('./my_finetuned_model')

model_path = './results/checkpoint-10000'
model = GPT2LMHeadModel.from_pretrained(model_path)

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

text_prompt = ""
generated_text = generator(text_prompt, max_length=100, num_return_sequences=1)
print(generated_text[0]['generated_text'])

def answer_crossword(clue, length):
    
    prompt = f"Length of the word is: {length} Clue: {clue} Answer:"

    response = generator(prompt, max_length=50, num_return_sequences=1)
    full_response = response[0]['generated_text']

    answer = full_response.split("Answer:")[1].strip().split('\n')[0].strip()

    return answer
# Random example but will test later on more (just like get a subset of the file)
answer_crossword('Harris in the Country Music Hall of Fame', 7)
