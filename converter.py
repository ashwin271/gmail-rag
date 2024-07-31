import json

def json_to_jsonl(input_file, output_file):
  """Converts a JSON file to a JSONL file.

  Args:
    input_file: Path to the input JSON file.
    output_file: Path to the output JSONL file.
  """

  with open(input_file, 'r') as json_file, open(output_file, 'w') as jsonl_file:
    data = json.load(json_file)
    for item in data:
      jsonl_file.write(json.dumps(item) + '\n')




if __name__ == "__main__":
    # Example usage:
    input_file = 'emails.json'
    output_file = 'data.jsonl'
    json_to_jsonl(input_file, output_file)
