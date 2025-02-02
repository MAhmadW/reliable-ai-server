# reliable-ai-server
An extensible FastAPI server that consumes AI API services (OpenAI by default) and switches the client based on statuses and incidents.

### Scaffolding

``` bash
pip install -r requirements.txt
```

### Environment Secrets

Make a .env and populate it with the API keys for your AI clients. An .env.example is present to get started with OpenAI and Perplexity.

### Running the Server

Development

``` bash
fastapi dev
```

Production

``` bash
fastapi run
```


