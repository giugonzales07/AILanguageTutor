from src.tools import create_tools
from src.db import init_db

def test_valid_type_appears_in_progress(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _, log_error, get_progress = create_tools("A", db_path=db)

    log_error("articles", "She is engineer", "She is an engineer")
    log_error("articles", "She is at engineer", "She is an engineer")
    log_error("articles", "She is on engineer", "She is an engineer")

    assert "articles: 3" in get_progress()

def test_unknown_type_becomes_other(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _, log_error, get_progress = create_tools("A", db_path=db)

    log_error("past tense", "She goed to school", "She went to school")

    assert "other: 1" in get_progress()

def test_new_session_has_no_errors(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _, _, get_progress = create_tools("A", db_path=db)

    assert "Nenhum erro" in get_progress()

def test_sessions_are_isolated(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _, log_error_a, get_progress_a = create_tools("A", db_path=db)
    _, _, get_progress_b = create_tools("B", db_path=db)

    log_error_a("past tense", "She goed to school", "She went to school")

    assert "other: 1" in get_progress_a()
    assert "Nenhum erro" in get_progress_b()

def test_error_type_is_normalized(tmp_path):
    db = tmp_path / "test.db"
    init_db(db)
    _, log_error_a, get_progress_a = create_tools("A", db_path=db)
    _, log_error_b, get_progress_b = create_tools("B", db_path=db)

    log_error_a("Articles", "She is engineer", "She is an engineer")
    log_error_b("  articles", "She is engineer", "She is an engineer")

    assert "articles: 1" in get_progress_a()
    assert "articles: 1" in get_progress_b()