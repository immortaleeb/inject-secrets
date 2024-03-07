import pytest

from inject_secrets.tokenizer import tokenize, TokenizationError


def test_tokenize_returns_single_line_literal():
   assert tokenize("some literal text") == [("literal", "some literal text")]

def test_tokenize_returns_multi_line_literal():
   assert tokenize("first line\nsecond line") == [("literal", "first line\nsecond line")]

def test_tokenize_recognizes_single_secret_path():
    assert tokenize("{{ some://secret/path }}") == [("secret_path", "some://secret/path")]

def test_tokenize_recognizes_literal_followed_by_secret_path():
    assert tokenize("username: {{ op://vault/secret/username }}") == [
        ("literal", "username: "),
        ("secret_path", "op://vault/secret/username"),
    ]

def test_tokenize_recognizes_secret_path_followed_by_literal():
    assert tokenize("{{ op://vault/secret/username }} is your username") == [
        ("secret_path", "op://vault/secret/username"),
        ("literal", " is your username"),
    ]

def test_tokenize_fails_on_missing_right_delimiter():
    with pytest.raises(TokenizationError):
        tokenize("username: {{ op://vault/secret/username ")

def test_tokenize_recognizes_literal_followed_by_secret_path_multi_line():
    assert tokenize("""
username: {{ op://vault/secret/username }}
fixed: value
password: {{ op://vault/secret/password }}
""") == [
        ("literal", "\nusername: "),
        ("secret_path", "op://vault/secret/username"),
        ("literal", "\nfixed: value\npassword: "),
        ("secret_path", "op://vault/secret/password"),
        ("literal", "\n"),
    ]

