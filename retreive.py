from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#PDF vector store
vector_store  = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)

#stackoverflow vectorstore
faq_store = FAISS.load_local(
    "faq_index", embeddings, allow_dangerous_deserialization=True
)

def img_retrieve(page_num):
    folder_path = "extracted_images"  # Folder containing images

    prefix = str(page_num) + "_img"  # Prefix to match

    # Ensure folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return []

    # Fetch all files that start with the prefix
    image_files = [f for f in os.listdir(folder_path) if f.startswith(prefix)]
    
    # Convert filenames to full paths
    image_files = [os.path.join(folder_path, f) for f in image_files]
    print(image_files)
    if image_files:
        return image_files[0]
    else:
        return None


def retreive_context(query):
    
    #retreiving context for relevant context
    results = vector_store.similarity_search(
        query,
        k=3,

    )

    res_pages = []
    rel_context = " "
    for res in results:
        rel_context+=res.page_content
        # print(f"""page_number:{res.metadata["page_num"]}""")
        res_pages.append(res.metadata["page_num"])

    
    #retreiving context for faq
    results = faq_store.similarity_search(
    query,
    k=2,

    )
    faq_context = " "
    for res in results:
        faq_context+=res.page_content
        print(f"""url:{res.metadata["url"]}""")
        print(faq_context)


    # Call function for each page number in res_pages
    images = []
    for page in res_pages:
        page=page+1
        temp = img_retrieve(page)
        if temp:
            images.append(temp)
        else:
            continue
    return rel_context,images,faq_context