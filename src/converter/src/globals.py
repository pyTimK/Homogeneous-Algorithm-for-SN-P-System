import json
import os
import xmltodict
import yaml

from src.converter.src.classes.Format import Format

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

XML = Format(
    path=os.path.join(DATA_PATH, "xml"),
    extension="xml",
    read_function=lambda s: xmltodict.parse(s)["content"],
    write_function=lambda d: xmltodict.unparse(
        d, pretty=True, newl="\n", indent=" " * 4
    ),
)

JSON = Format(
    path=os.path.join(DATA_PATH, "json"),
    extension="json",
    read_function=lambda s: json.loads(s),
    write_function=lambda d: json.dumps(d, indent=2),
)

YAML = Format(
    path=os.path.join(DATA_PATH, "yaml"),
    extension="yaml",
    read_function=lambda s: yaml.load(s, Loader=yaml.Loader),
    write_function=lambda d: yaml.dump(d, sort_keys=False, indent=2),
)

LOG = Format(
    path=os.path.join(DATA_PATH, "log"),
    extension="log",
    read_function=lambda _: {},
    write_function=lambda _: "",
)
