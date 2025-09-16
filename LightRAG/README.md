# LightRAG

This folder contains code and resources for working with the LightRAG framework.

## Workflow: PDF → Images → Markdown → LightRAG

1. **PDF to Images**: PDF files are placed in the `pdf/` directory. The `parse_pdf_image_to_markdown.ipynb` notebook processes each PDF, converting every page into an image (optionally cropping headers/footers for clarity).

2. **Images to Markdown**: Each page image is sent to an LLM (such as Mistral or Ollama) with a prompt, and the model generates a markdown representation of the page content. The resulting markdown is saved in the `md/` directory.

3. **Markdown to LightRAG**: The markdown files are then ingested by the LightRAG pipeline (see `kg_lightrag.ipynb`). LightRAG processes the markdown, generates embeddings, and stores them for efficient retrieval and question answering.

4. **Querying**: With the data indexed, you can use LightRAG to query the ingested content, leveraging the power of retrieval-augmented generation for downstream tasks.

This flow enables structured extraction and semantic search over complex PDF documents using state-of-the-art LLMs and RAG techniques.
