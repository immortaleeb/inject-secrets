from typing import IO, List

from .tokenizer import tokenize
from .resolve import SecretProvider, resolve_secret

def inject(*, template: str, providers: List[SecretProvider], file: IO):
    tokenization_result = tokenize(template)

    for token_type, token in tokenization_result:
        match token_type:
            case 'literal':
                file.write(token)
            case 'secret_path':
                secret = resolve_secret(token, providers)
                file.write(secret)
            case _:
                raise RuntimeError(f"Unknown token type {token_type}")

