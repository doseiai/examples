import os
from tempfile import NamedTemporaryFile

import chromadb
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredAPIFileLoader
from dotenv import load_dotenv

from fastapi import UploadFile, File, FastAPI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

load_dotenv()
app = FastAPI()

chroma_client = chromadb.HttpClient(host="localhost", port="8081")


@app.put("/ingest")
async def ingest(file: UploadFile = File(..., alias="file")):

    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    unstructured_url = os.getenv("UNSTRUCTURED_API_BASE_URL")
    loader = UnstructuredAPIFileLoader(
        temp_file_path,
        url=f"{unstructured_url}/general/v0/general",
        strategy="fast",
        mode="paged"
    )
    documents = loader.load()
    documents = [Document(page_content=document.page_content) for document in documents]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=2)
    docs = text_splitter.split_documents(documents)

    Chroma.from_documents(docs, embedding=OpenAIEmbeddings(), client=chroma_client)
    return documents


@app.get("/ask")
async def read_item(question: str):
    retriever = Chroma(client=chroma_client, embedding_function=OpenAIEmbeddings()).as_retriever()
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
    return qa.run(query=question)
