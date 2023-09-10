"""Load html from files, clean up, split, ingest into Weaviate."""

from langchain.docstore.document import Document
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from langchain.schema.runnable import Runnable
import requests
import weaviate
import os
import time
from dotenv import load_dotenv

load_dotenv()

def _add_documents(docs: list[Document]) -> bool:
    client = weaviate.Client(url=os.environ["WEAVIATE_URL"],
                             auth_client_secret=weaviate.AuthApiKey(api_key=os.environ["WEAVIATE_API_KEY"]))
    client.schema.delete_class("LangChain_newest_idx") # delete the class if it already exists

    embeddings = OpenAIEmbeddings(chunk_size=200)
    weav = Weaviate(client=client, index_name="LangChain_newest_idx", text_key="text", embedding=embeddings, by_text=False)

    batch_size = 100 # to handle batch size limit 
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        res = weav.add_documents(batch)
        print(f"i: {i} res: {res}")
    
    return True

def _split_documents(docs: list[Document]) -> list[Document]:
    headers_to_split_on = [
        ("#", "Header1"),
        ("##", "Header2"),
        ("###", "Header3"),
        ("####", "Header4"),
        ("#####", "Header5"),
    ]

    documents = []
    
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    for d in docs:
        md_header_splits = markdown_splitter.split_text(d.page_content)

        # Appending the header values into the documentation.
        # This seems producing better result in vector search
        for d in md_header_splits:
            metadata_str = ""
            if d.metadata:
                for h in headers_to_split_on:
                    val = d.metadata.get(h[1])
                    metadata_str += val if val else ""
                    metadata_str += " "
            d.page_content = metadata_str + "\n" + d.page_content
            documents.append(d)

    return documents

def _transform_documents(docs: list[Document]) -> list[Document]:
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    return docs_transformed

def _load_documents() -> list[Document]:
    urls = ["https://wiki.supercombo.gg/w/Street_Fighter_6/Blanka",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Cammy",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Chun-Li",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Dee_Jay",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Dhalsim",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/E.Honda",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Guile",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Jamie",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/JP",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Juri",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Ken",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Kimberly",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Lily",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Luke",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Manon",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Marisa",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Rashid",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Ryu",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Zangief",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Controls",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/HUD",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Offense",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Defense",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Movement",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Game_Data",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/Glossary",
            "https://wiki.supercombo.gg/w/Street_Fighter_6/FAQ"]

    documents = []

    for u in urls:
        response = requests.get(u)
        
        if response.status_code != 200:
            raise Exception(f"Requst failed with a status code: {response.status_code}. URL: {u}")

        page_content = response.content.decode('utf-8')
        documents.append(Document(page_content=page_content))

    return documents

def ingest_docs():
    docs = _load_documents()
    docs = _transform_documents(docs)
    docs = _split_documents(docs)
    _add_documents(docs)
    
if __name__ == "__main__":
    ingest_docs()