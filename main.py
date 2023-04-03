from src.classes.snp_system import Snp_system
from src.services.file_manager import FileManager
from src.algorithms.homogenize import homogenize


def main():
    # input_name = "naturally_greater_than_one"
    input_name = "DEMO"
    input_json = FileManager.load_xmp(f"./input/{input_name}.xmp")
    print(input_json)
    snp_system = Snp_system(input_json)
    homogenize(snp_system)
    output_name = f"./output/homogenized_{input_name}.xmp"
    FileManager.save_xmp(output_name, snp_system.to_xmp())
    print(f"Saved result to {output_name}")



if __name__ == "__main__":
    main()


