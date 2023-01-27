from collections import OrderedDict
from typing import Any
from src.classes.snp_system import Snp_system
from src.services.file_manager import FileManager
from src.algorithms.homogenize import homogenize


def main():
    input_json = FileManager.load_xmp("./input/test.xmp")
    snp_system = Snp_system(input_json)
    homogenize(snp_system)
    FileManager.save_xmp("./output/test_homogenized.xmp", snp_system.to_xmp())


    # FileManager.save_json("./output/fk.json", input_json)





if __name__ == "__main__":
    main()

    # print(snp_system.get_set_of_rule_transition_set())

    # print("-------------------R")
    # print(R)
