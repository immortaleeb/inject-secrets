from inject_secrets.resolve import NamedSecretProvider
from inject_secrets.load_providers import load_providers
from inject_secrets.providers.onepassword import OnePasswordProvider
from inject_secrets.providers.bitwarden import BitwardenCliProvider

def test_load_providers():
    providers = load_providers({
        'providers': {
            'op': 'inject_secrets.providers.onepassword:OnePasswordProvider',
            'bw': 'inject_secrets.providers.bitwarden:BitwardenCliProvider',
        },
    })

    assert len(providers) == 2
    assert isinstance(providers[0], NamedSecretProvider)
    assert isinstance(providers[0].resolver, OnePasswordProvider)
    assert isinstance(providers[1], NamedSecretProvider)
    assert isinstance(providers[1].resolver, BitwardenCliProvider)

def test_load_providers_passes_config_to_provider():
    providers = load_providers({
        'providers': {
            'toml': 'inject_secrets.providers.toml:TomlProvider',
        },
        'provider_config': {
            'toml': {
                'file': 'tests/secrets.toml',
            }
        },
    })

    assert providers[0].resolver.secrets == {
        'secret1': 'value-1',
        'secret2': 'value-2',
    }

