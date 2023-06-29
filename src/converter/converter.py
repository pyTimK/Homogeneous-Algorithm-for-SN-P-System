
from src.converter.src.classes.Format import Format
from src.converter.src.parsers import parse_dict_xml, parse_dict
from src.converter.src.globals import XML, JSON, YAML


def convert(str_input: str, from_format: Format, to_format: Format) -> str:
    d = from_format.read_function(str_input)
    system = parse_dict_xml(d) if from_format == XML else parse_dict(d)
    d = system.to_dict_xml() if to_format == XML else system.to_dict()
    return to_format.write_function(d)