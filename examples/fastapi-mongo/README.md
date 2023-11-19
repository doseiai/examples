# FastAPI with MongoDB Example
This directory is a brief example of a FastAPI app with MongoDB that can be deployed to Dosei with zero configuration.

<a href="https://dosei.ai/new/clone?source_full_name=doseiai/dosei&path=examples/fastapi-mongo&branch=main&env=MONGODB_URL" target="_blank" rel="noopener noreferrer">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://dosei.ai/badge.png">
  <img height="50px" alt="Deploy on Dosei button" src="https://dosei.com/badge.png"/>
</picture>
</a>

## Getting started
How to run this example locally

### Install dependencies

```bash
poetry install
```

### Populate the .env file with your MongoDB URL.
We recommend [MongoDB Atlas](https://www.mongodb.com/atlas/database). Their free tier includes:
- 512MB to 5GB of storage
- Shared RAM
- No credit card required to start

### Run it

1. Spawn your poetry virtual environment
```bash
poetry shell
```

2. Spin up the Todo FastAPI Server
```bash
uvicorn todo.main:app --reload
```
