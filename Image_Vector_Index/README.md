# Image Vector Index

This module demonstrates how to build a text-to-image retrieval system using vector embeddings and FAISS.

## What It Does
- Loads images from a directory
- Computes image embeddings using a pretrained vision model (`nomic-ai/nomic-embed-vision-v1.5`)
- Builds a FAISS index for fast similarity search
- Encodes a text query using a matching text model (`nomic-ai/nomic-embed-text-v1.5`)
- Retrieves the top-k most similar images to a text query

## How It Works
1. **Image Embedding**: Each image is processed by a vision transformer to produce a vector embedding.
2. **Indexing**: All image embeddings are added to a FAISS index for efficient nearest neighbor search.
3. **Text Query**: A text query is embedded using a compatible text transformer.
4. **Retrieval**: The text embedding is used to search the FAISS index and return the most similar images.

## Requirements
- Python 3.8+
- torch
- numpy
- faiss
- Pillow
- transformers

Install dependencies:
```bash
pip install torch numpy faiss-cpu pillow transformers
```

## Usage
- Place your images in an `images/` folder inside this directory.
- Run the notebook `image_vector_index.ipynb` to build the index and try text-to-image search.

## Example
- Query: `"winter village with snow"`
- The notebook will print the top-5 most similar images and their distances.

---
This is a simple, local demo of multimodal retrieval using open-source models and FAISS. For larger datasets or production use, consider batching, GPU acceleration, and more advanced indexing options.
