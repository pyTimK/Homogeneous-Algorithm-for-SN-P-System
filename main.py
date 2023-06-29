from src.classes.snp_system import SnpSystem
from src.services.file_manager import FileManager
from src.algorithms.homogenize_prime_released_spike_scaling import homogenize_prime_released_spike_scaling
from src.algorithms.homogenize_type_2_scaling import homogenize_type_2_scaling
from src.types.snp_system_dict import SnpSystemDict
from src.algorithms.auto_layout import auto_layout
from enum import Enum
from typing import List
import timeit
from src.converter.converter import convert
from src.converter.src.globals import XML, JSON, YAML
import xmltodict

# Set to true to print the actual running time of the homogeneous algorithm used
get_actual_running_time = False
test_runs = 500
# input_name = "DEMO.xmp"
input_name = "bit_adder([0,0,3,0,0]).json"
format = JSON if input_name.split(".")[1] == 'json' else YAML if input_name.split(".")[1] == 'yaml' else XML

class ScalingType(Enum):
    """
    Used to determine the scaling type to be used
    """
    TYPE_2_SUBSYSTEM_SCALING = 0
    RELEASED_SPIKE_SCALING = 1



def main():
    """
    The main function
    """

    # Set the name of the input xmp file to be used. It must be inside the `input` folder

    # Set the scaling type to be used
    scaling_type = ScalingType.TYPE_2_SUBSYSTEM_SCALING

    # Load the file
    input_str = FileManager.load_file(f"./input/{input_name}")

    if format == JSON:
        input_str = convert(input_str, JSON, XML)
    elif format == YAML:
        input_str = convert(input_str, YAML, XML)

    # Load the SNP System dictionary from the input xmp file
    snp_system_dict = SnpSystemDict(xmltodict.parse(input_str))

    # Print the input SNP System
    # #!!print(snp_system_dict)


    # Perform the homogenization algorithm with the right scaling type
    if get_actual_running_time:
        snp_system = homogenize(snp_system_dict, ScalingType.TYPE_2_SUBSYSTEM_SCALING)
        snp_system = homogenize(snp_system_dict, ScalingType.RELEASED_SPIKE_SCALING)
    
    else:
        snp_system = homogenize(snp_system_dict, scaling_type)

    # Auto layout the graph when there are new neurons (multiplier neurons)
    if scaling_type == ScalingType.TYPE_2_SUBSYSTEM_SCALING:
        auto_layout(snp_system)

    # Save the homogenized SN P system into an xmp file. This can be found in the `output` folder
    output_name = f"./output/homogenized_{input_name}"

    output_str = snp_system.to_xmp()
    if format == JSON:
        output_str = convert(output_str, XML, JSON)
    elif format == YAML:
        output_str = convert(output_str, XML, YAML)

    FileManager.save_xmp(output_name, output_str)

    # Print the homogenized SN P System
    print("\nHOMOGENIZED SNP SYSTEM: ")
    print(snp_system)


    # Print the location of the saved file
    #!!print(f"Saved result to {output_name}")



def homogenize(snp_system_dict: SnpSystemDict, scaling_type: ScalingType) -> SnpSystem:
    """
    Homogenizes an SN P system based on the scaling type
    """

    # Get the average actual running time
    #!!print(f"\n--- Acutal Running Time of Homogenization (Type 2 Subsystem Scaling) ---")

    # Parse the SN P system dictionary into its equivalent SnpSystem object
    snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)

    # Print the input SN P system
    #!!print("\nINPUT SNP SYSTEM: ")
    #!!print(snp_system)

    if scaling_type == ScalingType.TYPE_2_SUBSYSTEM_SCALING:
        # Homogenize SN P system using Type 2 Subsystem Scaling
        if get_actual_running_time:
            running_time = timeit.timeit(lambda: homogenize_type_2_scaling(snp_system),  number=test_runs) #! O(n^3k)
        
        else:
            homogenize_type_2_scaling(snp_system)
    else:
        # Homogenize SN P system using Released Spike Scaling
        if get_actual_running_time:
            running_time = timeit.timeit(lambda: homogenize_prime_released_spike_scaling(snp_system),  number=test_runs) #! O(nk)
        
        else:
            homogenize_prime_released_spike_scaling(snp_system)

    # Get the end time if getting actual running time and print the time difference

    if get_actual_running_time:
        average_time = running_time / test_runs * 1000
        print(f"\n{input_name} ({scaling_type}): {average_time} ms")
    
    return snp_system

if __name__ == "__main__":
    main()

