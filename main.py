from collections import OrderedDict
from typing import Any
from src.classes.snp_system import Snp_system
from src.services.file_manager import FileManager
from src.algorithms.homogenize import homogenize


def main():
    input_json = FileManager.load_xmp("./input/test.xmp")
    snp_system = Snp_system(input_json)
    R = homogenize(snp_system)
    print(R)


    FileManager.save_json("./output/fk.json", input_json)





if __name__ == "__main__":
    main()

    # print(snp_system.get_set_of_rule_transition_set())

    # print("-------------------R")
    # print(R)
