import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.schema import Document
from langchain.document_loaders import DirectoryLoader
import os
import shutil

class RAGFramework:

    CHROMA_PATH = "chroma"
    DATA_PATH = "data/articles"
    def __init__(self):
        self.model = ChatOllama(model="mistral")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
             maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )
        self.vector_store = None
        self.retriever = None
        self.chain = None

    def load_documents_from_disk(self):
        loader = DirectoryLoader(self.DATA_PATH, glob="*.txt")
        documents = loader.load()
        return documents
    def split_text(self, documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        document = chunks[10]
        print(document.page_content)
        print(document.metadata)

        return chunks

    def save_to_chroma(self, chunks: list[Document]):
        # Clear out the database first.
        if os.path.exists(self.CHROMA_PATH):
            shutil.rmtree(self.CHROMA_PATH)

        # Create a new DB from the documents.
        db = Chroma.from_documents(
            chunks, FastEmbedEmbeddings(), persist_directory=self.CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {self.CHROMA_PATH}.")
        return db

    def load_documents(self):
        # chunks = self.text_splitter.split_documents(texts)  # Correct method to split text
        # self.vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        documents = self.load_documents_from_disk()
        chunks = self.split_text(documents)
        self.vector_store = self.save_to_chroma(chunks)
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 5,  # Retrieve top 5 documents
                "score_threshold": 0.2,  # Lower threshold for broader retrieval
            },
        )

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())


    def ask(self, query: str):
        if not self.chain:
            return "The system is not ready. Please load the documents first."
        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None

def retrieve_articles(urls):
    texts = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_text = soup.find('article').text
        texts.append(article_text)
    return texts
