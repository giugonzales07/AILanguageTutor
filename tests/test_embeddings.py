import json
from src.embeddings import process_and_embed

def test_process_and_embed(monkeypatch, tmp_path):
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.json"

    data = [
        {
            "title": "English vocabulary",
            "content": "Walk means caminhar."
        }
    ]

    # Simula a leitura da base
    monkeypatch.setattr(
        "src.embeddings.load_json",
        lambda file: data.copy()
    )

    # Simula a geração do embedding
    monkeypatch.setattr(
        "src.embeddings.embed_file",
        lambda title, content: [0.1, 0.2, 0.3]
    )

    process_and_embed(str(input_file), str(output_file))

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as file:
        result = json.load(file)

    assert len(result) == 1
    assert result[0]["title"] == "English vocabulary"
    assert result[0]["embeddings"] == [0.1, 0.2, 0.3]