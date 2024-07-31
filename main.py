import json
import time
import pathway as pw
from common.embedder import embeddings, index_embeddings

# reading from jsonl
# class FileStreamSubject(pw.io.python.ConnectorSubject):
#     def run(self):
#         with open("data.jsonl") as file:
#             for line in file:
#                 data = json.loads(line)
#                 self.next(**data)
#                 time.sleep(1)



class InputSchema(pw.Schema):
    idf: str = pw.column_definition(primary_key=True)    
    subject: str
    sender: str
    date: str
    body: str 


email_data = pw.io.csv.read(
  'output.csv',
  schema=InputSchema,
)




embedded_data = embeddings(context=email_data, data_to_embed=email_data.subject)

pw.io.csv.write(embedded_data, "embedded_data.csv")

index = index_embeddings(embedded_data)




# pw.io.csv.write(table, "output.csv")

pw.run()