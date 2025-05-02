from src.retrieval import find_text_relevant

def test_find_text_relevant():
    # Test data
    query = "Não sei falar caminhar em inglês, poderia me ajudar a traduzir?"
    json_file = "data/how_teach_embeddings.json"
    model = "models/embedding-001"

    # Call the function to find relevant text
    result = find_text_relevant(query, json_file, model)

    # View the result
    print("Result:", result)

    # Check if the result is a list and not empty
    assert isinstance(result, list), "Result is not a list."
    assert len(result) > 0, "Result is empty."

    # Check if the first element of the result is a string
    assert isinstance(result[0], str), "First element of the result is not a string."