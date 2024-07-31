import pathway as pw
import os
from dotenv import load_dotenv
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
from pathway.xpacks.llm.parsers import ParseUnstructured
from pathway.xpacks.llm.splitters import TokenCountSplitter

load_dotenv()

dropbox_folder_path = os.environ.get("DROPBOX_LOCAL_FOLDER_PATH", "/usr/local/documents")

class InputSchema(pw.Schema):
    idf: str = pw.column_definition(primary_key=True)    
    subject: str
    sender: str
    date: str
    body: str

def run(host, port):
    # Given a user search query
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Read email data from CSV
    email_data = pw.io.csv.read(
        'output.csv',
        schema=InputSchema,
    )

    # Compute embeddings for each email using the subject
    embedded_data = embeddings(context=email_data, data_to_embed=email_data.subject)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()

class QueryInputSchema(pw.Schema):
    query: str

if __name__ == "__main__":
    run("0.0.0.0", 8080)  # Changed to 0.0.0.0 to allow external connections