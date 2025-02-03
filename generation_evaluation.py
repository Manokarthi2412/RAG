from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_cosine_similarity(actual_text, generated_text):
    actual_embedding = model.encode(actual_text, convert_to_tensor=True)
    generated_embedding = model.encode(generated_text, convert_to_tensor=True)

    similarity = cosine_similarity([actual_embedding.cpu().numpy()], [generated_embedding.cpu().numpy()])[0][0]
    
    return similarity

eval_df = pd.read_csv(r"expected_answers.csv")
responses_list = []
accuracy = []
for ind in range(len(responses_list)):
    actual = eval_df["Expected Answer"][ind]
    generated = responses_list[ind]
    
    similarity_score = compute_cosine_similarity(actual, generated)
    accuracy.append(100*similarity_score)
    print(f"Cosine Similarity: {100*similarity_score:.4f}")
