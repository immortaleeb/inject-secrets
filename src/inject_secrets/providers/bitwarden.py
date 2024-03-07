import subprocess as sp

from ..resolve import SecretProvider

class BitwardenCliProvider(SecretProvider):
    def can_resolve(self, provider: str, path: str) -> bool:
        return provider == 'bw'

    def resolve(self, provider: str, path: str) -> str:
        secret, obj = path.split('/')

        if not (obj in ['username', 'password']):
            raise RuntimeException(f"Unknown object of type '{obj}' in bitwarden secret '{provider}://{path}'")

        proc = sp.run(['bw', 'get', obj, secret], stdout=sp.PIPE, text=True)
        proc.check_returncode()
        return proc.stdout.strip()

