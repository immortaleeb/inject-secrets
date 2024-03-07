import importlib

from typing import List

from .resolve import SecretProvider, NamedSecretProvider

def load_class(class_path):
    module_path, class_name = class_path.split(':')
    module = importlib.import_module(module_path)
    clazz = getattr(module, class_name)
    return clazz()


def load_providers(config: dict) -> List[SecretProvider]:
    return [NamedSecretProvider(provider_name, load_class(class_path)) for provider_name, class_path in config.items()]

