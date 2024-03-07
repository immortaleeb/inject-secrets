import subprocess as sp

from ..resolve import SecretProvider

class OnePasswordProvider(SecretProvider):
    def resolve(self, provider: str, path: str) -> str:
        proc = sp.run(['op', 'read', f'op://{path}'], stdout=sp.PIPE, text=True)
        proc.check_returncode()
        return proc.stdout.strip()

