from collections import OrderedDict
from typing import Any
from src.classes.snp_system import Snp_system
from src.services.file_manager import FileManager
from src.algorithms.homogenize import homogenize
from src.classes.period_constants_pair import PeriodConstantsPair
from src.classes.constants import Constants


def main():
    input_json = FileManager.load_xmp("./input/test.xmp")
    snp_system = Snp_system(input_json)
    homogenize(snp_system)
    FileManager.save_xmp("./output/test_homogenized.xmp", snp_system.to_xmp())



if __name__ == "__main__":
    main()
