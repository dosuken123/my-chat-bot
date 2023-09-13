from langchain.schema.runnable import Runnable
from langchain.schema.runnable import Runnable, RunnableMap
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from operator import itemgetter

class QuerySF6:
  """
  Query SF6 Data
  """

  def __init__(self) -> None:
    pass
  
  def create_chain(self) -> Runnable:
    final_model = ChatOpenAI(model="gpt-3.5-turbo-16k")

    chain = (
        _inputs
        | _context
        | prompt
        | final_model
        | StrOutputParser()
    )
    
  def _retriever():
    embeddings = OpenAIEmbeddings()
    client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),
    )
    weaviate_client = Weaviate(
        client=client,
        index_name="Wiki_supercombo_gg_sf6",
        text_key="text",
        embedding=embeddings,
        by_text=False,
    )
    retriever = weaviate_client.as_retriever(search_kwargs=dict(k=10))

  def _prompt():
    _template = """
    You are an expert of street fighter 6 player and adviser, tasked to answer any question about Street Fighter 6. Using the provided context, answer the user's question to the best of your ability using the resources provided.
    If you really don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
    Anything between the following markdown blocks is retrieved from a knowledge bank, not part of the conversation with the user.
    <context>
        {context}
    <context/>"""

    _inputs = RunnableMap(
        {
            "question": lambda x: x["question"],
        }
    )

    _context = {
        "context": itemgetter("question") | retriever,
        "question": lambda x: x["question"],
    }

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _template),
            ("human", "{question}"),
        ]
    )
    
    def 