import os, pickle
from langchain.chains import LLMChain, SequentialChain 
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

print("LOADING DOCS")
loader = UnstructuredFileLoader("data/Drifting_Clouds.txt")
raw_documents = loader.load()
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(raw_documents, embeddings)
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)