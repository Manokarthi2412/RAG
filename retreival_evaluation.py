from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pandas as pd

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#PDF vector store
vector_store  = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)

def retreive(query):
    results = vector_store.similarity_search(
        query,
        k=3,
    
    )
    rel_context = []
    for res in results:
        rel_context.append(res.page_content)
    print(rel_context)
    return rel_context


df = pd.read_csv(r"retreival_evaluation_data.csv")


retreived_context=[]
for ind in range(len(df)):
    query = df["User Query"][ind]
    retreive(query)
    retreived_context.append(retreive(query))


def any_keyword_present(paragraph, keywords):
    return any(keyword.lower() in paragraph.lower() for keyword in keywords)

retrieval_scores = 0
for i in range(len(retreived_context)):
    para = " "
    keywords = df["Retrieval Keywords"][i].split(", ") 
    for j in retreived_context[i]:
        para+=j

    if any_keyword_present(para, keywords):
        retrieval_scores+=1
    else:
        continue
    
print(f"Retrieval Evaluation for all user queries : {round(100*(retrieval_scores)/10)}.00%")
