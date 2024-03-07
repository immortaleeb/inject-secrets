import importlib

from typing import List

from .resolve import SecretProvider, NamedSecretProvider

def load_class(class_path, provider_config):
    module_path, class_name = class_path.split(':')
    module = importlib.import_module(module_path)
    clazz = getattr(module, class_name)
    return clazz() if provider_config is None else clazz(config=provider_config)

def load_provider(provider_name, class_path, provider_config):
    return NamedSecretProvider(provider_name, load_class(class_path, provider_config))


def load_providers(config: dict) -> List[SecretProvider]:
    provider_config = config.get('provider_config', {})
    return [
        load_provider(provider_name, class_path, provider_config.get(provider_name, None))
        for provider_name, class_path in config['providers'].items()
    ]

