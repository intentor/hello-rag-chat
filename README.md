# Hello RAG Chat

This application retrieves the contents of a webpage to use it as context when asking questions to a chatbot using Llama-3 LLM.

It was created to demonstrate RAG (Retrieval Augmented Generation), a technique to provide context to an LLM so it can be more accurate when generating results.

Inspired by the article [How to Build a Local RAG App with Llama 3 (Complete Guide)](<http://anakin.ai/blog/llama-3-rag-locally/>).

## Setup

Download and install [Ollama](https://www.ollama.com), a framework to interact with LLMs.

After installing Ollama, you have to download the Llama-3 LLM:

```bash
ollama pull llama3
```

In order to use a language model, you have to start Ollama:

```bash
ollama serve
# or
make serve
```

In a new terminal, run the command below to setup the Python virtual envrinment and dependencies:

```bash
make setup
```

## Running the app

```bash
make
# or
make run
```

The chat page will open in your browser. You can enter a URL to generate context for the conversation and start asking questions about it after loading.
