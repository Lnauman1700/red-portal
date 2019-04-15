from portal import create_app


def test_config():
    app = create_app()
    assert not app.testing
    assert create_app({'TESTING': True}).testing

