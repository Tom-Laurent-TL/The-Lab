
# Llama_Index

This folder demonstrates a workflow for extracting knowledge from PDFs and enabling advanced retrieval-augmented generation (RAG) using LlamaIndex.

## Workflow: PDF → Images → Markdown → LlamaIndex

1. **PDF to Images**: Place your PDF files in the `pdf/` directory. Each PDF is processed, and every page is converted into an image (optionally cropping headers/footers for clarity).

2. **Images to Markdown**: Each page image is sent to an LLM (such as Mistral or Ollama) with a prompt, and the model generates a markdown representation of the page content. The resulting markdown is saved in the `md/` directory.

3. **Markdown to LlamaIndex**: The markdown files are then ingested by the LlamaIndex pipeline (see `kg_llama_index.ipynb`). LlamaIndex processes the markdown, builds a knowledge graph, and creates an index for efficient retrieval and question answering.

4. **Querying**: With the data indexed, you can use LlamaIndex to query the ingested content, leveraging retrieval-augmented generation for downstream tasks. You can also compare different LLMs (Ollama, Mistral) for RAG performance using the provided notebooks.

## What is a Knowledge Graph?

A knowledge graph is a structured representation of information where entities (such as people, places, or concepts) are connected by relationships. In this workflow, after extracting content from PDFs and converting it to markdown, LlamaIndex analyzes the text to identify key entities and the relationships between them. These are organized into a graph structure, making it possible to:
- Visualize and explore connections between concepts in your documents
- Enable more precise and context-aware retrieval for question answering
- Support advanced analytics and reasoning over your data

The knowledge graph serves as the backbone for retrieval-augmented generation (RAG), allowing LLMs to answer questions using both the original content and the structured relationships extracted from your documents.

## Contents
- `kg_llama_index.ipynb`: Notebook for building a knowledge graph and RAG pipeline with LlamaIndex.
- `ollama_mistral_comparison.ipynb`: Notebook comparing Ollama and Mistral models for RAG tasks.
- `md/`: Contains markdown files generated or used by the notebooks.
- `pdf/`: Contains PDF files used as data sources.

## Requirements
- Python 3.8+
- LlamaIndex
- Ollama (for local LLMs)
- Mistral SDK
- Jupyter Notebook

## Usage
1. Place your PDF files in the `pdf/` folder.
2. Use the workflow to convert PDFs to images, then to markdown, and finally ingest into LlamaIndex.
3. Open and run `kg_llama_index.ipynb` to build the index and run RAG queries.
4. Use `ollama_mistral_comparison.ipynb` to compare model outputs.

---
This folder is a template for experimenting with document extraction, knowledge graph construction, and RAG pipelines using LlamaIndex and multiple LLM backends.
