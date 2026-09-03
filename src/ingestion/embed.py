from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def embed(chunks: List):
   embeddings = model.encode(
        chunks,
        convert_to_numpy=True
   )
   return embeddings
if __name__ == '__main__':