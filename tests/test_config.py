from enterprise_support import config


def test_create_chat_model_loads_project_env_file(monkeypatch, tmp_path):
    package_dir = tmp_path / "src" / "enterprise_support"
    package_dir.mkdir(parents=True)
    (tmp_path / ".env").write_text(
        "OPENAI_API_KEY=test-key\nOPENAI_MODEL=test-model\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(config, "__file__", str(package_dir / "config.py"))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    client = object()
    monkeypatch.setattr("openai.OpenAI", lambda api_key: client)

    model = config.create_chat_model()

    assert model.client is client
    assert model.model == "test-model"
