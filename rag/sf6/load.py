from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
import requests

class Load:
  """
  Document loaders

  Load documents from many different sources.
  LangChain provides over a 100 different document loaders as well as integrations with other major providers in the space, like AirByte and Unstructured.
  We provide integrations to load all types of documents (html, PDF, code) from all types of locations (private s3 buckets, public websites).
  """
  
  def __init__(self) -> None:
    pass
    
  def execute(self) -> None:
    source = self._sources[0]
    
    response = requests.get(source)
    
    if response.status_code == 200:
      print("Successful response")
    else:
      print("Requst failed with a status code: ", response.status_code)
  
  def _sources(self):
    ["https://wiki.supercombo.gg/w/Street_Fighter_6/Luke"]