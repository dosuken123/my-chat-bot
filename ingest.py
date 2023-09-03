"""Load html from files, clean up, split, ingest into Weaviate."""
from bs4 import BeautifulSoup as Soup
import weaviate
import os
from git import Repo
import shutil

from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL=os.environ["WEAVIATE_URL"]
WEAVIATE_API_KEY=os.environ["WEAVIATE_API_KEY"]

def ingest_repo():
    repo_path = os.path.join(os.getcwd(), "test_repo")
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    repo = Repo.clone_from("https://github.com/langchain-ai/langchain", to_path=repo_path)

    loader = GenericLoader.from_filesystem(
        repo_path+"/libs/langchain/langchain",
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
    )
    documents_repo = loader.load()

    python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, 
                                                                chunk_size=2000, 
                                                                chunk_overlap=200)
    texts = python_splitter.split_documents(documents_repo)
    return texts

def ingest_docs():
    """Get documents from web pages."""

    urls = [
        # "https://www.streetfighter.com/6/character", # OK
        # "https://www.streetfighter.com/6/character/rashid/frame",
        "https://wiki.supercombo.gg/w/Street_Fighter_6/Luke" # OK
        # https://streetfighter.fandom.com/wiki/Juri_Han#Biography
        # "https://api.python.langchain.com/en/latest/api_reference.html#module-langchain",
        # "https://python.langchain.com/docs/get_started", 
        # "https://python.langchain.com/docs/use_cases",
        # "https://python.langchain.com/docs/integrations",
        # "https://python.langchain.com/docs/modules", 
        # "https://python.langchain.com/docs/guides",
        # "https://python.langchain.com/docs/ecosystem",
        # "https://python.langchain.com/docs/additional_resources",
        # "https://python.langchain.com/docs/community",
    ]
    
    exclude_dirs = [
        "Frame_data", "Combos", "Resources", "Matchups", "Strategy", "Data"
    ]

    documents = []
    extractor = lambda x: Soup(x, "lxml").text
    for j, url in enumerate(urls):
        # max_depth = 2 if j == 0 else 10
        max_depth = 1
        loader = RecursiveUrlLoader(url=url,
                                    max_depth=max_depth,
                                    extractor=extractor,
                                    prevent_outside=True,
                                    ensure_trailing_slash=False,
                                    exclude_dirs=exclude_dirs)
        temp_docs = loader.load()           
        # print(f"temp_docs: {temp_docs}")
        documents += temp_docs
        print("Loaded", len(temp_docs), "documents from", url)
    
    print("Loaded", len(documents), "documents from all URLs")
    
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(documents)
    
    print("Loaded", len(documents), "documents from all URLs")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    print('before splitting', len(docs_transformed))
    docs_transformed = text_splitter.split_documents(docs_transformed)
    print('after splitting', len(docs_transformed))
    
    print('Debuging... end')
    return

    # repo_docs = ingest_repo()
    # docs_transformed += repo_docs
        
    # # OPTION TO PICKLE
    # print("pickle.dumping..")
    # import pickle
    # with open('docs_transformed.pkl', 'wb') as f:
    #     pickle.dump(docs_transformed, f)
        
    # with open('docs_transformed.pkl', 'rb') as f:
    #     docs_transformed = pickle.load(f)
    
    client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY))
    client.schema.delete_class("LangChain_newest_idx") # delete the class if it already exists

    embeddings = OpenAIEmbeddings(chunk_size=200) # rate limit
    weav = Weaviate(client=client, index_name="LangChain_newest_idx", text_key="text", embedding=embeddings, by_text=False)

    batch_size = 100 # to handle batch size limit 
    for i in range(0, len(docs_transformed), batch_size):
        batch = docs_transformed[i:i+batch_size]
        print(f"i: {i}")
        # import pdb; pdb.set_trace()
        weav.add_documents(batch)
        # Weaviate.add_documents(batch, embeddings, client=client, by_text=False, index_name="LangChain_newest_idx")

    print("LangChain now has this many vectors", client.query.aggregate("LangChain_newest_idx").with_meta_count().do())
    
if __name__ == "__main__":
    ingest_docs()