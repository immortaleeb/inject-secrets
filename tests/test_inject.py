import pytest

from inject_secrets.resolve import SecretProvider
from inject_secrets.inject import inject

class FakeFile:
    def __init__(self):
        self.output = ""

    def write(self, output):
        self.output += output

class FakeSecretProvider(SecretProvider):
    def can_resolve(self, provider: str, path: str):
        return True

    def resolve(self, provider: str, path: str):
        if path == "vault/secret/username":
            return "USERNAME"
        elif path == "vault/secret/password":
            return "PASSWORD"
        return "SECRET"

class OpProvider(SecretProvider):
    def can_resolve(self, provider: str, path: str):
        return provider == 'op'

    def resolve(self, provider: str, path: str):
        return 'OP_SECRET'

class BwProvider(SecretProvider):
    def can_resolve(self, provider: str, path: str):
        return provider == 'bw'

    def resolve(self, provider: str, path: str):
        return 'BW_SECRET'


class NoneSecretProvider(SecretProvider):
    def can_resolve(self, provider: str, path: str):
        return False

    def resolve(self, provider: str, path: str):
        raise "Should not be called"

@pytest.fixture
def fake_file():
    return FakeFile()

@pytest.fixture
def fake_provider():
    return FakeSecretProvider()

@pytest.fixture
def template():
    return """
username: {{ op://vault/secret/username }}
password: {{ bw://vault/secret/password }}
"""

def test_inject_fails_when_no_provider_can_resolve_secret_path(fake_file, template):
    with pytest.raises(RuntimeError):
        inject(template=template, providers=[NoneSecretProvider()], file=fake_file)

def test_inject_resolves_secrets_using_single_provider(fake_file, fake_provider, template):
   inject(template=template, providers=[fake_provider], file=fake_file)

   assert fake_file.output == """
username: USERNAME
password: PASSWORD
"""

def test_inject_resolves_secrets_using_multiple_providers(fake_file, template):
   inject(template=template, providers=[OpProvider(), BwProvider()], file=fake_file)

   assert fake_file.output == """
username: OP_SECRET
password: BW_SECRET
"""

