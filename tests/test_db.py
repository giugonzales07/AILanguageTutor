from src.db import init_db, save_error, top_errors


def test_top_errors_sorted_by_count(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)

    for _ in range(3):
        save_error(db, "A", "articles", "She is engineer", "She is an engineer")
    save_error(db, "A", "modals", "She can to swim", "She can swim")

    assert top_errors(db, "A") == [("articles", 3), ("modals", 1)]


def test_session_isolation(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)

    save_error(db, "A", "articles", "She is engineer", "She is an engineer")

    assert top_errors(db, "B") == []


def test_session_without_errors_returns_empty_list(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)

    assert top_errors(db, "A") == []


def test_limit_of_results(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)

    for tipo in ["articles", "modals", "much-many", "verb-to-be"]:
        save_error(db, "A", tipo, "frase", "correcao")

    assert len(top_errors(db, "A", limit=2)) == 2