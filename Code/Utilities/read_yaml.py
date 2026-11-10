from typing import LiteralString

import yaml

def load_yaml_content(yaml_route: LiteralString) -> dict:
    with open(yaml_route, 'r', encoding='utf-8') as fd:
        return yaml.load(fd, Loader=yaml.FullLoader)