import requests
from bs4 import BeautifulSoup


from langchain_community.embeddings import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


question=[]

def stack_extract(url):     
    
    response = requests.get(url)
    
    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      title = soup.find("h1").text.strip() if soup.find("h1") else "Title not found"
    
      
    

    accept_ans_elements = soup.find_all(class_="answer js-answer accepted-answer js-accepted-answer")
       
    if accept_ans_elements:
        for accept_ans_element in accept_ans_elements:
            post_body_elements = accept_ans_element.find_all(class_="s-prose js-post-body")
            
            for post_body_element in post_body_elements :
              temp=post_body_element.get_text()
              temp=temp.replace('\n','')
              print(title)
              print(temp)
              return title,temp
    else:
        return 

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

faq_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

faq_store.save_local("faq_index")

url= "url/for/stackoverflow/page"
result = stack_extract(url)
title,text=result
documents=[]
documents.append(Document(page_content=str(title)+str(text), metadata={"url":url}))
faq_store.add_documents(documents=documents)


