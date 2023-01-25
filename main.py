from collections import OrderedDict
from typing import Any
from src.classes.snp_system import Snp_system
from src.services.file_manager import FileManager
from src.algorithms.homogenize import homogenize


def main():
    input_json = FileManager.load_xmp("./input/test.xmp")
    snp_system = Snp_system(input_json)
    homogenize(snp_system.get_unique_rule_transition_set())
    print ()

    FileManager.save_json("./output/fk.json", input_json)



def xmp_to_snp(input_xmp: OrderedDict[str, Any]):
    return 





if __name__ == "__main__":
    main()