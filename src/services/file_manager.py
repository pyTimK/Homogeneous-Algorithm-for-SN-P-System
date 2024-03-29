from typing import OrderedDict, Any
import json
import xmltodict

class FileManager:
    @staticmethod
    def load_file(name: str) -> str:
        """
        Load the input file
        """
        with open(name) as input_file:
            return input_file.read()
        
    @staticmethod
    def load_xmp(name: str) -> OrderedDict[str, Any]:
        """
        Load the input file and convert from xmp to python dictionary
        """
        with open(name) as xmp_input_file:
            xmp_str = xmp_input_file.read()
            return xmltodict.parse(xmp_str)

    @staticmethod
    def save_xmp(name: str, xmp: str):
        """
        Save the xmp string to a file
        """
        with open(name, "w") as xmp_file:
            xmp_file.write(xmp)
