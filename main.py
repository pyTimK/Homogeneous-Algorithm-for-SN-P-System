from src.classes.snp_system import SnpSystem
from src.services.file_manager import FileManager
from src.algorithms.homogenize_prime_released_spike_scaling import homogenize_prime_released_spike_scaling
from src.algorithms.homogenize_type_2_scaling import homogenize_type_2_scaling
from src.types.snp_system_dict import SnpSystemDict
from src.algorithms.auto_layout import auto_layout
from enum import Enum


class ScalingType(Enum):
    """
    Used to determine the scaling type to be used
    """
    TYPE_2_SUBSYSTEM_SCALING = 1
    RELEASED_SPIKE_SCALING = 2



def main():
    """
    The main function
    """

    # Set the name of the input xmp file to be used. It must be inside the `input` folder
    input_name = "homogenized_DEMO_with_input"

    # Set the scaling type to be used
    scaling_type = ScalingType.TYPE_2_SUBSYSTEM_SCALING

    # Load the SNP System dictionary from the input xmp file
    snp_system_dict = SnpSystemDict(FileManager.load_xmp(f"./input/{input_name}.xmp"))

    # Print the input SNP System
    print(snp_system_dict)

    # Parse the SN P system dictionary into its equivalent SnpSystem object
    snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)

    # Perform the homogenization algorithm with the right scaling type
    if scaling_type == ScalingType.TYPE_2_SUBSYSTEM_SCALING:
        homogenize_type_2_scaling(snp_system)  #! O(n^2k)
        auto_layout(snp_system)

    elif scaling_type == ScalingType.RELEASED_SPIKE_SCALING:
        homogenize_prime_released_spike_scaling(snp_system)  #! O(nk)
    
    else:
        raise ValueError("Invalid Scaling type")

    # Save the homogenized SN P system into an xmp file. This can be found in the `output` folder
    output_name = f"./output/homogenized_{input_name}.xmp"
    FileManager.save_xmp(output_name, snp_system.to_xmp())

    # Print the location of the saved file
    print(f"Saved result to {output_name}")



if __name__ == "__main__":
    main()

