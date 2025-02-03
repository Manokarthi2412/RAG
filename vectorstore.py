from langchain_community.embeddings import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import fitz 
import os
import extract
import moviepy as mp
import speech_recognition as sr

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)



embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

vector_store.save_local("faiss_index")

def chunk_docs(page_text):
    documents = []
    for page_num,page in enumerate(page_text):
        documents.append(Document(page_content=page, metadata={"page_num":page_num}))
    documents = documents[7:]
    vector_store.add_documents(documents=documents)


def video_text(speech_text):
    documents=[]
    documents.append(Document(page_content=speech_text, metadata={"page_num":-1}))
    vector_store.add_documents(documents=documents)

def main():
    pages = extract.main()
    chunk_docs(pages)

    video = mp.VideoFileClip("uploads/inputvideo.mp4")
    video.audio.write_audiofile("output_audio.wav")
    r = sr.Recognizer()
    filename = "output_audio.wav"
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        speech_text = r.recognize_google(audio_data)

    video_text(speech_text)