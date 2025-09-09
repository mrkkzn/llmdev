import pytest
from authenticator import Authenticator

@pytest.fixture
def authenticator():
    auth = Authenticator()
    yield auth
    auth.__init__

@pytest.mark.parametrize("username, password, expected", [
    ("testname1", "passw0rd", {"testname1": "passw0rd"}),
    ("testname2", "PASSW0RD", {"testname2": "PASSW0RD"}),
])
def test_register_OK(authenticator, username, password, expected):
    authenticator.register(username, password)
    assert authenticator.users == expected
    assert authenticator.users.get(username) == password

def test_registor_ERROR(authenticator):
    username = "username"
    password = "password"
    authenticator.register(username, password)

    with pytest.raises(ValueError, match="エラー: ユーザーは既に存在します。"):
        authenticator.register(username, password)

@pytest.mark.parametrize("username, password", [
    ("testname1", "passw0rd"),
    ("testname2", "PASSW0RD"),
])
def test_login_OK(authenticator, username, password, expected = "ログイン成功"):
    authenticator.register(username, password)
    assert authenticator.login(username, password) == expected

@pytest.mark.parametrize("username, password", [
    ("foo", "password"),
    ("username", "var"),
    ("foo", "var"),
])
def test_login_ERROR(authenticator, username, password):
    authenticator.register("username", "password")

    with pytest.raises(ValueError, match="エラー: ユーザー名またはパスワードが正しくありません"):
        authenticator.login(username, password)