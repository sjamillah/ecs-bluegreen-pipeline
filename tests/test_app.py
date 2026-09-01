"""Route-level tests for the Typerush app.

Run locally:   PYTHONPATH=app pytest tests/ -q
These run in CI before any AWS step, so a broken commit fails in seconds
instead of after a four-minute deployment.
"""
import app as application


def client():
    return application.app.test_client()


# --- /health -----------------------------------------------------------
# The ALB target group, CodeDeploy and the Dockerfile HEALTHCHECK all depend
# on this returning 200. If it breaks, every deployment fails.

def test_health_returns_200_and_ok():
    r = client().get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_health_reports_a_version():
    assert "version" in client().get("/health").get_json()


# --- / -----------------------------------------------------------------

def test_home_renders_the_app():
    r = client().get("/")
    assert r.status_code == 200
    assert b"Typerush" in r.data


# --- /api/words --------------------------------------------------------

def test_words_default_count():
    r = client().get("/api/words")
    assert r.status_code == 200
    assert len(r.get_json()["words"]) == 80


def test_words_respects_requested_count():
    assert len(client().get("/api/words?count=25").get_json()["words"]) == 25


def test_words_count_is_clamped_both_ways():
    assert len(client().get("/api/words?count=9999").get_json()["words"]) == 300
    assert len(client().get("/api/words?count=1").get_json()["words"]) == 10


def test_words_survives_a_junk_count():
    r = client().get("/api/words?count=abc")
    assert r.status_code == 200
    assert len(r.get_json()["words"]) == 80


def test_words_are_all_strings():
    assert all(isinstance(w, str) and w for w in client().get("/api/words").get_json()["words"])


# --- word bank ---------------------------------------------------------

def test_word_bank_has_no_duplicates():
    from words import WORDS
    assert len(WORDS) == len(set(WORDS))
