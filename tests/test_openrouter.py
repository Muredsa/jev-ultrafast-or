"""Offline tests for the OpenRouter compatibility adapter."""

from unittest.mock import Mock

from jev_ultrafast import model, openrouter


def test_openrouter_key_maps_to_upstream_environment(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    monkeypatch.setenv("TEXT_MODEL_API_KEY", "")
    monkeypatch.delenv("TYPESAFE_MODEL", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.setenv("JEV_MODEL", "typesafe/jev-1.13")

    openrouter._sync_environment()

    assert openrouter.os.environ["TYPESAFE_API_KEY"] == "sk-or-test"
    assert openrouter.os.environ["TEXT_MODEL_API_KEY"] == "sk-or-test"
    assert openrouter.os.environ["TYPESAFE_MODEL"] == "typesafe/jev-1.13"


def test_native_systemone_url_is_redirected_to_openrouter(monkeypatch):
    response = Mock(status_code=200, is_error=False)
    response.json.return_value = {"answers": {}}
    post = Mock(return_value=response)
    monkeypatch.setattr(model.CLIENT, "post", post)

    result = model.post_json(
        "https://api.typesafe.ai/v1/systemone",
        "sk-or-test",
        {"model": "~typesafe/jev-latest", "state": {}, "questions": {}},
    )

    assert result == {"answers": {}}
    assert post.call_args.args[0] == openrouter.OPENROUTER_DECISIONS_URL
