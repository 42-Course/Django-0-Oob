#!/usr/bin/python3
import sys
import os
import re

import settings


def get_values():
    """Collect every non-dunder variable defined in settings.py."""
    return {key: value for key, value in vars(settings).items()
            if not key.startswith('__')}


def render(path):
    if not path.endswith('.template'):
        print("Error: input file must have a .template extension.",
              file=sys.stderr)
        return 1
    if not os.path.isfile(path):
        print("Error: file '{}' does not exist.".format(path),
              file=sys.stderr)
        return 1

    with open(path, 'r') as f:
        content = f.read()

    values = get_values()

    def replace(match):
        key = match.group(1)
        if key in values:
            return str(values[key])
        return match.group(0)

    rendered = re.sub(r'\{(\w+)\}', replace, content)

    output = os.path.splitext(path)[0] + '.html'
    with open(output, 'w') as f:
        f.write(rendered)
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <file.template>", file=sys.stderr)
        sys.exit(1)
    sys.exit(render(sys.argv[1]))
