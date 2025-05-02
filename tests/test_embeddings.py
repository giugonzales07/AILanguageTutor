from src.embeddings import process_and_embed
import os
import json

def test_process_and_embed():
    input_json_file = "data/how_teach.json"
    output_json_file = "data/how_teach_embeddings.json"
    model = "models/embedding-001"

    # Call the function to process and embed the JSON file
    process_and_embed(input_json_file, output_json_file, model)

    # Check if the output file was created
    assert os.path.exists(output_json_file), "Output JSON file was not created."

    # Load the output JSON file and check its contents
    with open(output_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        assert isinstance(data, list), "Output JSON file does not contain a list."
        assert len(data) > 0, "Output JSON file is empty."