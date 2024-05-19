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

# Load tokenizer and model
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


# Initialize the generator with the fine-tuned model and standard tokenizer
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# Generate text
text_prompt = ""
generated_text = generator(text_prompt, max_length=100, num_return_sequences=1)
print(generated_text[0]['generated_text'])

def answer_crossword(clue, length):
    # Format the prompt as expected by the model, e.g., "Clue: <clue> Answer:"
    prompt = f"Length of the word is: {length} Clue: {clue} Answer:"

    # Use the generator to generate text. Adjust max_length based on expected answer length
    response = generator(prompt, max_length=50, num_return_sequences=1)
    full_response = response[0]['generated_text']

    # Optional: Process the response to extract the answer part
    # This assumes the model's output format is consistent and includes the answer following "Answer:"
    answer = full_response.split("Answer:")[1].strip().split('\n')[0].strip()

    return answer

answer_crossword('Harris in the Country Music Hall of Fame', 7)