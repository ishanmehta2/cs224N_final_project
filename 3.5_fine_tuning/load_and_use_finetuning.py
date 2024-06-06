# Install if needed
import openai

# hiding because I don't want our key stolen LOL
openai.api_key = ""

# this is what I called the file in the github. If you run this on colab, this is fine. If on VSCode, change the filepath
with open('fine_tuned_model_name.txt', 'r') as f:
    fine_tuned_model = f.read().strip()

def generate_unique_completions(prompt, model, num_completions=5, max_tokens=50):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        n=num_completions * 2,  
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

# Call it
prompt = "Tries for a role, 5, R___S"
completions = generate_unique_completions(prompt, fine_tuned_model, num_completions=5)
for i, completion in enumerate(completions, 1):
    print(f"Completion {i}: {completion}")


