
# I downloaded sentence_transformers and then this should work

from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load a bi-encoder model
bi_encoder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def encode_texts(bi_encoder, texts):
    return bi_encoder.encode(texts)

def calculate_similarity(clue_embedding, answer_embeddings):
    return util.dot_score(clue_embedding, answer_embeddings)[0].cpu().numpy()

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# Example usage
clue = "Fennel or sweet cicely"
answers = ["HERB", "SPICE", "ANISE", "PLANT", "VEGETABLE"]

clue_embedding = encode_texts(bi_encoder, [clue])[0]
answer_embeddings = encode_texts(bi_encoder, answers)

similarity_scores = calculate_similarity(clue_embedding, answer_embeddings)
probabilities = softmax(similarity_scores)

answer_probabilities = list(zip(answers, probabilities))

# Print the answers with their probabilities
for answer, probability in answer_probabilities:
    print(f"Answer: {answer}, Probability: {probability:.4f}")
