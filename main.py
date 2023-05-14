from src.classes.snp_system import SnpSystem
from src.services.file_manager import FileManager
from src.algorithms.modified_homogenize import modified_homogenize
from src.algorithms.homogenize_type_2_scaling import homogenize_type_2_scaling
from src.types.snp_system_dict import SnpSystemDict


def main():
    """
    The main function 
    """
    # input_name = "naturally_greater_than_one"
    input_name = "DEMO_with_input"
    snp_system_dict = SnpSystemDict(FileManager.load_xmp(f"./input/{input_name}.xmp"))
    print(snp_system_dict)
    snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)
    # modified_homogenize(snp_system)  #! O(nk)
    homogenize_type_2_scaling(snp_system)
    output_name = f"./output/homogenized_{input_name}.xmp"
    FileManager.save_xmp(output_name, snp_system.to_xmp())
    print(f"Saved result to {output_name}")



if __name__ == "__main__":
    main()


