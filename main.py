from src.classes.snp_system import SnpSystem
from src.services.file_manager import FileManager
from src.algorithms.homogenize_prime_released_spike_scaling import homogenize_prime_released_spike_scaling
from src.algorithms.homogenize_type_2_scaling import homogenize_type_2_scaling
from src.types.snp_system_dict import SnpSystemDict
from src.algorithms.auto_layout import auto_layout
from enum import Enum
from typing import List
import time

# Set to true to print the actual running time of the homogeneous algorithm used
get_actual_running_time = False
test_runs = 1

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
    input_name = "myex4"

    # Set the scaling type to be used
    scaling_type = ScalingType.TYPE_2_SUBSYSTEM_SCALING

    # Load the SNP System dictionary from the input xmp file
    snp_system_dict = SnpSystemDict(FileManager.load_xmp(f"./input/{input_name}.xmp"))

    # Print the input SNP System
    # print(snp_system_dict)


    # Perform the homogenization algorithm with the right scaling type
    snp_system = homogenize(snp_system_dict, scaling_type)

    # Auto layout the graph when there are new neurons (multiplier neurons)
    if scaling_type == ScalingType.TYPE_2_SUBSYSTEM_SCALING:
        auto_layout(snp_system)

    # Save the homogenized SN P system into an xmp file. This can be found in the `output` folder
    output_name = f"./output/homogenized_{input_name}.xmp"
    FileManager.save_xmp(output_name, snp_system.to_xmp())

    # Print the homogenized SN P System
    # print("\nHOMOGENIZED SNP SYSTEM: ")
    # print(snp_system)


    # Print the location of the saved file
    print(f"Saved result to {output_name}")



def homogenize(snp_system_dict: SnpSystemDict, scaling_type: ScalingType) -> SnpSystem:
    """
    Homogenizes an SN P system based on the scaling type
    """

    # Get the average actual running time
    print(f"\n--- Acutal Running Time of Homogenization (Type 2 Subsystem Scaling) ---")
    running_times: List[int] = []

    for i in range(test_runs):
        # Parse the SN P system dictionary into its equivalent SnpSystem object
        snp_system = SnpSystem.from_dict(snp_system_dict)  #! O(n^2 + nk + nt)

        # Print the input SN P system
        if i == 0:
            print("\nINPUT SNP SYSTEM: ")
            print(snp_system)

        # Get the start time if getting actual running time
        if get_actual_running_time:
            start_time = time.time()

        if scaling_type == ScalingType.TYPE_2_SUBSYSTEM_SCALING:
            # Homogenize SN P system using Type 2 Subsystem Scaling
            homogenize_type_2_scaling(snp_system)  #! O(n^2k)
        else:
            # Homogenize SN P system using Released Spike Scaling
            homogenize_prime_released_spike_scaling(snp_system)  #! O(nk)

        # Get the end time if getting actual running time and print the time difference
        if get_actual_running_time:
            end_time = time.time()
            running_time = end_time - start_time
            print(f"> {running_time} seconds")
            running_times.append(running_time)
    
    if get_actual_running_time:
        ave_running_time = sum(running_times) / len(running_times)
        print(f"\nAverage running time: {ave_running_time} seconds")

    return snp_system

if __name__ == "__main__":
    main()

