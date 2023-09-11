- [x] Run chat-langchain locally
- [-] Use Langchain from the fork (Otherwise I can't track the changes in LangChain)
- [x] Understand RAG https://python.langchain.com/docs/modules/data_connection/
- [x] Use collabo too
- [x] Define Ingest SF6 Class
  - [x] Convert HTML to nice markdown
  - [x] Split Markdown
  - [x] Check how embedding is computed. Are headers used? => Only `text`. Metadata is not used.
  - [x] Test including metadata into the text.
  - [x] Test top 3 similarily search, not just one.
- [x] Define Query SF6 Class
  - [x] Prepare prompt
  - [x] Infer 
- [x] Optimize the document loading part - Currently, the documents parses seem skewed.
- [x] Enable Coplilot
- [-] Apply for LangSmmith  
- [x] Resolve mac VScode can't resolve package links.
- [x] Make sure it runs locally
- [x] Deploy the chat app!
- [x] Fix the chat doesn't work in mobile
- [ ] Setup DNS A record
- [ ] Read https://docs.langchain.com/docs/
- [ ] Read https://python.langchain.com/docs/get_started/introduction
  - [ ] Understand the chain executions https://docs.langchain.com/docs/components/chains/chain

## Running tests

`python -m pytest tests/`
`python -m pytest --pdb  tests/`

## Build docker image

`docker build -t sf6-qa-chat .`

```
docker login
docker tag sf6-qa-chat:latest shinyamaeda/sf6-qa-chat:latest
docker push shinyamaeda/sf6-qa-chat:latest
```

## Run docker image

```shell
docker run -p 3000:3000 \
           -p 8080:8080 \
           -e WEAVIATE_URL="<input-your-secret>" \
           -e WEAVIATE_API_KEY="<input-your-secret>" \
           -e OPENAI_API_KEY="<input-your-secret>" \
           sf6-qa-chat:latest
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
    `NEXT_PUBLIC_API_BASE_URL` = "<backend-endpoint>"
