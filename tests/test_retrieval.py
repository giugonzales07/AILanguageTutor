from src.retrieval import find_query

def test_find_query_returns_most_relevant_content():
    data = [
        {
            "id": "walk",
            "content": "Walk means caminhar.",
            "embeddings": [1, 0]
        },
        {
            "id": "apple",
            "content": "Apple means maçã.",
            "embeddings": [0, 1]
        },
        {
            "id": "walking",
            "content": "Walking is an activity.",
            "embeddings": [0.9, 0.1]
        }
    ]

    query_embedding = [1, 0]

    result = find_query(query_embedding, data, top_k=1)

    assert result[0]["id"] == "walk"
    assert result[0]["content"] == "Walk means caminhar."
    


def test_find_query_returns_top_k_results():
    data = [
        {"id": "walk", "content": "Walk means caminhar.", "embeddings": [1, 0]},
        {"id": "apple", "content": "Apple means maçã.", "embeddings": [0, 1]},
        {"id": "walking", "content": "Walking is an activity.", "embeddings": [0.9, 0.1]}
    ]

    result = find_query([1, 0], data, top_k=2)

    assert len(result) == 2
    assert result[0]["id"] == "walk"
    assert result[0]["content"] == "Walk means caminhar."
    assert result[1]["id"] == "walking"
    assert result[1]["content"] == "Walking is an activity."