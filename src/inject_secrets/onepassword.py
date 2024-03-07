import subprocess as sp

from .resolve import SecretProvider

class OnePasswordProvider(SecretProvider):
    def __init__(self):
        pass

    def can_resolve(self, provider: str, path: str) -> bool:
        return provider == 'op'

    def resolve(self, provider: str, path: str) -> str:
        proc = sp.run(['op', 'read', f'op://{path}'], stdout=sp.PIPE, text=True)
        return proc.stdout.strip()

