import sys
import tomllib

from pathlib import Path

from .load_providers import load_providers
from .inject import inject
from .providers.onepassword import OnePasswordProvider
from .providers.bitwarden import BitwardenCliProvider

def print_help(*, file=sys.stdout):
    print("Injects secrets into a templated file")
    print(f"Usage: {sys.argv[0]} template_file")


def parse_arguments():
    if len(sys.argv) < 2:
        print("Missing argument: template_file", file=sys.stderr)
        print_help(file=sys.stderr)
        exit(1)

    template_file = Path(sys.argv[1])

    if not (template_file.exists() and template_file.is_file()):
        print(f"Could not find file '{template_file}'", file=sys.stderr)
        exit(2)

    return {
        'template_file': template_file,
    }

def load_config():
    config_file = Path('inject-secrets.toml')
    if not (config_file.exists() and config_file.is_file()):
        print(f"Could not find config file. Please create a 'inject-secrets.toml' in the working directory", file=sys.stderr)
        exit(3)

    with config_file.open('rb') as f:
        return tomllib.load(f)


def main():
    args = parse_arguments()
    config = load_config()

    template_file = args['template_file']
    with template_file.open('r') as f:
        template = f.read()

    providers = load_providers(config)

    inject(template=template, providers=providers, file=sys.stdout)


if __name__ == '__main__':
    main()

