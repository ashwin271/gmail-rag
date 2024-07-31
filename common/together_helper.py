from dotenv import load_dotenv
import os
import pathway as pw
from together import Together

load_dotenv()

api_key = os.environ.get("TOGETHER_API_KEY")
embedding_model = os.environ.get("TOGETHER_EMBEDDING_MODEL", "togethercomputer/m2-bert-80M-8k-retrieval")

client = Together(api_key=api_key)

def together_embedder(data):
    @pw.udf
    def embed(text):
        response = client.embeddings.create(
            model=embedding_model,
            input=text
        )
        return response.data[0].embedding

    return embed(data)