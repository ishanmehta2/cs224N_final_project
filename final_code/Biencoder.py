from sentence_transformers import SentenceTransformer, util
import numpy as np

bi_encoder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def biencoder(clue, answers):
    def encode_texts(bi_encoder, texts):
        return bi_encoder.encode(texts)
    
    def calculate_similarity(clue_embedding, answer_embeddings):
        return util.dot_score(clue_embedding, answer_embeddings)[0].cpu().numpy()
    
    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
    
    clue_embedding = encode_texts(bi_encoder, [clue])[0]
    answer_embeddings = encode_texts(bi_encoder, answers)
    
    similarity_scores = calculate_similarity(clue_embedding, answer_embeddings)
    probabilities = softmax(similarity_scores)
    
    answer_probabilities = {answer: prob for answer, prob in zip(answers, probabilities)}
    
    return answer_probabilities
