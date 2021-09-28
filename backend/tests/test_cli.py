def test_shell_context_processor(app):
    with app.app_context():
        shell_globals = app.shell_context_processors[0]()
        assert "app" in shell_globals
        assert "client" in shell_globals
        assert "db" in shell_globals
