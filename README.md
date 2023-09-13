# SF6 QA App

This repo is an implementation of a locally hosted chatbot specifically focused on question answering over the [Street Figher 6](https://www.streetfighter.com/6).
Built with [LangChain](https://github.com/hwchase17/langchain/), [FastAPI](https://fastapi.tiangolo.com/), and [Next.js](https://nextjs.org).

This project was forked from [Chat LangChain](https://github.com/langchain-ai/chat-langchain).

The app leverages LangChain's streaming support and async API to update the page in real time for multiple users.

## ✅ Running locally

1. Install backend dependencies: `pip install -r requirements.txt`.
1. Run `python ingest.py` to ingest LangChain docs data into the Weaviate vectorstore (only needs to be done once).
   1. You can use other [Document Loaders](https://langchain.readthedocs.io/en/latest/modules/document_loaders.html) to load your own data into the vectorstore.
1. Run the backend with `make start`.
   1. Make sure to enter your environment variables to configure the application:
   ```
   export OPENAI_API_KEY=
   export WEAVIATE_URL=
   export WEAVIATE_API_KEY=

   # for tracing
   export LANGCHAIN_TRACING_V2=true
   export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
   export LANGCHAIN_API_KEY=
   export LANGCHAIN_PROJECT=
   ```
1. Install frontend dependencies by running `cd frontend`, then `yarn`.
1. Run the frontend with `yarn dev` for frontend.
1. Open [localhost:3000](http://localhost:3000) in your browser.

### Using docker compose

```
docker compose build
docker compose up
```

then access `http://localhost:3000/`

## 📚 Technical description

There are two components: ingestion and question-answering.

Ingestion has the following steps:

1. Pull html from documentation site as well as the Github Codebase
2. Load html with LangChain's [RecursiveURLLoader Loader](https://python.langchain.com/docs/integrations/document_loaders/recursive_url_loader)
2. Transform html to text with [Html2TextTransformer](https://python.langchain.com/docs/integrations/document_transformers/html2text)
3. Split documents with LangChain's [RecursiveCharacterTextSplitter](https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html)
4. Create a vectorstore of embeddings, using LangChain's [Weaviate vectorstore wrapper](https://python.langchain.com/docs/integrations/vectorstores/weaviate) (with OpenAI's embeddings).

Question-Answering has the following steps, all handled by [OpenAIFunctionsAgent](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent):

1. Given the chat history and new user input, determine what a standalone question would be (using GPT-3.5).
2. Given that standalone question, look up relevant documents from the vectorstore.
3. Pass the standalone question and relevant documents to GPT-4 to generate and stream the final answer.
4. Generate a trace URL for the current chat session, as well as the endpoint to collect feedback.

## Running tests

`python -m pytest tests/`
`python -m pytest --pdb  tests/`

## 🚀 Deployment

Deploy the frontend Next.js app as a serverless Edge function on Vercel [by clicking here]().
You'll need to populate the `NEXT_PUBLIC_API_BASE_URL` environment variable with the base URL you've deployed the backend under (no trailing slash!).

### Build and push docker image

```
docker login
docker compose build
docker tag sf6-qa-chat-backend:latest shinyamaeda/sf6-qa-chat-backend:latest
docker push shinyamaeda/sf6-qa-chat-backend:latest
docker tag sf6-qa-chat-frontend:latest shinyamaeda/sf6-qa-chat-frontend:latest
docker push shinyamaeda/sf6-qa-chat-frontend:latest
```

## Deploy docker image

Use CloudRun

Backend:
  variables:
    WEAVIATE_URL="<input-your-secret>"
    WEAVIATE_API_KEY="<input-your-secret>"
    OPENAI_API_KEY="<input-your-secret>"
Frontend:
  variables:
    `NEXT_PUBLIC_API_BASE_URL` = "<backend-public-endpoint>"
