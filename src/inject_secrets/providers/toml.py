import tomllib
from pathlib import Path

from ..resolve import SecretProvider

class TomlProvider(SecretProvider):
    def __init__(self, *, config):
        file = config['file']
        secrets_file = Path(file)
        if not (secrets_file.exists() and secrets_file.is_file()):
            raise RuntimeError(f"Could not find secrets file '{file}'")

        with secrets_file.open('rb') as f:
            self.secrets = tomllib.load(f)

    def resolve(self, provider: str, path: str) -> str:
        split_result = path.split('/')
        if len(split_result) == 1:
            return self.secrets[path]

        section, secret = split_result
        return self.secrets[section][secret]

