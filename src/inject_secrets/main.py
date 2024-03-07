import sys

from pathlib import Path

from .inject import inject
from .providers.onepassword import OnePasswordProvider
from .providers.bitwarden import BitwardenCliProvider

PROVIDERS = [OnePasswordProvider(), BitwardenCliProvider()]

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

def main():
    args = parse_arguments()
    template_file = args['template_file']

    with template_file.open('r') as f:
        template = f.read()

    inject(template=template, providers=PROVIDERS, file=sys.stdout)


if __name__ == '__main__':
    main()

