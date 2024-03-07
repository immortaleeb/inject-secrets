import re

from typing import Protocol, List, Optional, Tuple

class SecretProvider(Protocol):
    def can_resolve(self, provider: str, path: str) -> bool:
        return True

    def resolve(self, provider: str, path: str) -> str:
        pass

class NamedSecretProvider(SecretProvider):
    def __init__(self, name: str, resolver: SecretProvider):
        self.name = name
        self.resolver = resolver

    def can_resolve(self, provider: str, path: str) -> bool:
        return provider == self.name and self.resolver.can_resolve(provider, path)

    def resolve(self, provider: str, path: str) -> str:
        return self.resolver.resolve(provider, path)

def provider_which_can_resolve(provider_name: str, path: str, providers: List[SecretProvider]) -> Optional[SecretProvider]:
    return next(iter(provider for provider in providers if provider.can_resolve(provider_name, path)), None)

def parse_secret_path(path: str) -> Tuple[str, str]:
    match = re.fullmatch('([^: /]+)://(.*)', path)
    if not match:
        raise RuntimeError(f"Could not parse secret path '{path}'")

    return match.groups()


def resolve_secret(secret_path: str, providers: List[SecretProvider]) -> str:
    provider_name, path = parse_secret_path(secret_path)
    provider = provider_which_can_resolve(provider_name, path, providers)
    if not provider:
        raise RuntimeError(f"Could not find provider which can resolve {secret_path}")
    return provider.resolve(provider_name, path)

