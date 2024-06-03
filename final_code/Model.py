import openai 

openai.api_key = 'sk-proj-8oLvnNGJLnlgW4SQOoHwT3BlbkFJ8c24SWE59CoO4sTxlDC7'

with open('/Users/ohmpatel/Downloads/fine_tuned/fine_tuned_model_name.txt', 'r') as f:
    fine_tuned_model = f.read().strip()


def generate_unique_completions(prompt, model, num_completions=5, max_tokens=50):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        n=num_completions,  
        stop=None,
        temperature=0.9,  
        top_p=0.9  
    )
    completions = set()
    for choice in response['choices']:
        completions.add(choice['message']['content'].strip())
        if len(completions) >= num_completions:
            break
    
    return list(completions)[:num_completions]  # Return only the requested number of unique completions

