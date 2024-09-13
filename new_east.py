from utils import *  # Importing utility functions and variables
from bisect import bisect_right  # Importing bisect_right for binary search functionality

def get_concrete_weight():
    """
    Function to calculate concrete weight and concrete weight plus live load.
    The user inputs the unit weight of concrete, slab thickness, live load, and motorized option.
    Returns the final concrete weight plus live load.
    """
    
    # User input
    unit_weight_of_concrete = float(input("Please enter unit weight of concrete: "))
    thickness_of_slab = float(input("Please enter thickness of slab: "))
    suitable_live_load = float(input("Please enter suitable live load: "))
    is_motorized = input("Please choose Motorized (1) or non-motorized (2): ")

    # Validate motorized input
    while is_motorized not in ["1", "2"]:
        is_motorized = input("Invalid Option! Please choose Motorized (1) or Non-motorized (2): ")

    # Select options based on motorized or non-motorized choice
    final_option = motorized_options if is_motorized == "1" else non_motorized_options

    # Calculate and display concrete weight
    concrete_weight = round(unit_weight_of_concrete * thickness_of_slab, 2)
    print(f"Concrete Weight: {concrete_weight}")

    # Calculate and display concrete weight plus live load
    concrete_weight_plus_live_load = concrete_weight + suitable_live_load
    print(f"Concrete Weight plus Live Load: {concrete_weight_plus_live_load}")

    # Determine the final thickness by finding the next higher available option
    final_thickness = thickness_options[bisect_right(thickness_options, thickness_of_slab)]
    print(f"Final Thickness: {final_thickness}")

    # Adjust the concrete weight plus live load based on the final thickness option
    concrete_weight_plus_live_load = max(final_option[final_thickness], concrete_weight_plus_live_load)

    print(f"Final Concrete Weight plus Live Load: {concrete_weight_plus_live_load}\n")
    return concrete_weight_plus_live_load

def get_sheathing_info():
    """
    Function to gather sheathing details from the user, such as plywood or plyform choice,
    class type, and face grain orientation.
    Returns sheathing type (plywood or not), class, and face grain orientation.
    """
    
    # User input for sheathing type
    plywood_or_plyform = input("Please choose between Plywood (1) and Plyform (2): ")
    while plywood_or_plyform not in ["1", "2"]:
        plywood_or_plyform = input("Invalid option! Please choose between Plywood (1) and Plyform (2): ")

    is_plywood = plywood_or_plyform == "1"

    # If Plyform is selected, get the class of Plyform
    if not is_plywood:
        ply_class = input("Please choose between Class I (1), Class II (2), Structural I (3): ")
        while ply_class not in ["1", "2", "3"]:
            ply_class = input("Invalid Option! Please choose between Class I (1), Class II (2), Structural I (3): ")
    
    # If Plywood is selected, get the type of plywood
    else:
        ply_class = input("Please choose between Structural I and Marine (1), another class for different species (2): ")
        while ply_class not in ["1", "2"]:
            ply_class = input("Invalid Option! Please choose between Structural I and Marine (1), another class for different species(2): ")

    # Get the face grain orientation from the user
    is_face_grain_across = input("Please choose between face grain across (1) or along (2): ")
    while is_face_grain_across not in ["1", "2"]:
        is_face_grain_across = input("Invalid Option! Please choose between face grain across (1) or along (2): ")
    
    print()
    return is_plywood, ply_class, is_face_grain_across

def get_sheathing_thickness(is_plywood, ply_class, is_face_grain_across):
    """
    Function to gather the sheathing thickness and related parameters based on user input.
    Different options are provided for plyform, plywood, and species classes.
    Returns the final values and parameters used in further calculations.
    """
    
    # For Plyform sheathing
    if not is_plywood:
        input_plyform_thickness = float(input("Please enter plyform thickness: "))
        while input_plyform_thickness not in plyform_thickness:
            print(f"Invalid option. Only {', '.join(map(str, plyform_thickness))} are allowed.")
            input_plyform_thickness = float(input("Please enter plyform thickness: "))

        final_sheathing_thickness = input_plyform_thickness
        final_sheathing_weight = plyform_weight_by_thickness[final_sheathing_thickness]
        final_parameter = plyform_general_mapper[f"{ply_class}_{is_face_grain_across}"][final_sheathing_thickness]

    # For Plywood with different species
    elif ply_class == "2":
        input_species_thickness = float(input("Please enter different species thickness: "))
        while input_species_thickness not in different_species_thickness:
            print(f"Invalid option. Only {', '.join(map(str, different_species_thickness))} are allowed.")
            input_species_thickness = float(input("Please enter different species thickness: "))

        final_sheathing_thickness = input_species_thickness
        final_sheathing_weight = plywood_weight_different[final_sheathing_thickness]
        final_parameter = plywood_across_different[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_different[final_sheathing_thickness]

    # For Plywood with Structural/Marine type
    elif ply_class == "1":
        input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
        while input_structural_marine_thickness not in structural_marine_thickness:
            print(f"Invalid option. Only {', '.join(map(str, structural_marine_thickness))} are allowed.")
            input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
        final_sheathing_thickness = input_structural_marine_thickness
        final_sheathing_weight = plywood_weight_marine[final_sheathing_thickness]
        final_parameter = plywood_across_marine[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_marine[final_sheathing_thickness]

    # Output the results of the thickness calculations
    print(f"Final Sheathing Thickness: {final_sheathing_thickness}")
    print(f"Final Sheathing Weight: {final_sheathing_weight}")
    print(f"Final Parameters: {final_parameter}\n")

    shores_values = {}
    
    # Additional input required if plywood is selected
    if is_plywood:
        stress_group = int(input("Please choose stress group of plywood (1-6): "))
        while stress_group not in range(1, 7): 
            stress_group = int(input("Invalid option! Please choose stress group of plywood (1-6): "))

        final_stress = stress_of_plywood
        stress_grade_level = input("Please choose stress grade level S-1, 2, or 3: ")
        while stress_grade_level not in ["1", "2", "3"]:
            stress_grade_level = input("Invalid option! Please choose stress grade level S-1, 2, or 3: ")

        # Determine index based on stress grade level and wet/dry condition
        if stress_grade_level in ["1", "2"]:
            is_wet = input("Is it wet (1) or dry (2)? ")
            while is_wet not in ["1", "2"]:
                is_wet = input("Invalid option! Is it wet (1) or dry (2)? ")
            index = 0 if stress_grade_level == "1" and is_wet == "1" else 1 if stress_grade_level == "1" and is_wet == "2" else 2 if stress_grade_level == "2" and is_wet == "1" else 3
        else:
            is_wet = "2"
            index = 4

        # Assign final stress values
        for k, v in final_stress.items():
            if stress_group in v:
                shores_values[k] = v[stress_group][index]
        
        shores_values["Fs"] = rolling_shear_table[ply_class][index]

    # If Plyform is selected, assign stress values based on the class
    else:
        shores_values = plyform_stress[ply_class]

    # Output final values and return them
    print("Final Values:")
    for k, v in shores_values.items():
        print(f"{k}: {v}")

    return shores_values, final_parameter, final_sheathing_weight

def get_sheathing_distance(shores_values, final_parameter, concrete_weight_plus_live_load, is_plywood):
    """
    Function to calculate the optimal sheathing distance based on input parameters like 
    bending stress, shear stress, elasticity, concrete weight, and live load.
    Returns the number of spans, design span, and final distance between sheathing.
    """
    # Get number of spans from the user
    no_of_spans = input("Please enter number of spans (1-3): ")
    while no_of_spans not in ["1", "2", "3"]:
        no_of_spans = input("Invalid option! Please enter number of spans (1-3): ")

    no_of_spans = int(no_of_spans)

    # Bending stress (Fb), shear stress (Fs), and modulus of elasticity (E)
    fb = shores_values["Fb"]
    fs = shores_values["Fs"]
    E = shores_values["E"]

    print(f"fb: {fb:.2f}")
    
    # Shear factor based on plywood or plyform selection
    se_index = 2 if is_plywood else 1
    sheathing_se = final_parameter[se_index]

    rolling_shear = final_parameter[-1]  # Rolling shear value
    print(f"rs: {rolling_shear}")
    print(f"se: {sheathing_se}")
    print(f"wb: {concrete_weight_plus_live_load}")
    
    print(f"fs: {fs:.2f}")
    print(f"E: {E}")
    
    # Moment of inertia based on plywood or plyform selection
    i_index = 1 if is_plywood else 0
    final_parameter_i = final_parameter[i_index]
    print(f"I: {final_parameter_i:.2f}")

    # Design span input
    design_span = float(input("Enter design span (m): ")) * 1000  # Convert to millimeters

    # Calculate lb (based on bending stress and concrete weight)
    lb_constant = 120 if no_of_spans == 3 else 96
    lb = (((lb_constant * fb * sheathing_se) / concrete_weight_plus_live_load) ** 0.5) / 1000 

    # Calculate ls (based on shear stress and rolling shear)
    ls = (ls_constant_mapper[no_of_spans] * fs * rolling_shear) / (concrete_weight_plus_live_load * 1000)

    # Deflection constraints
    deflection_a_input = design_span / 360
    deflection_b_input = design_span / 16
    deflection_a_equation = ((1743 * E * final_parameter_i) / (360 * concrete_weight_plus_live_load)) ** (1/3) / 1000
    deflection_b_equation = ((1743 * E * final_parameter_i) / (16 * concrete_weight_plus_live_load)) ** (1/4) / 1000
    final_deflection_a = min(deflection_a_input, deflection_a_equation)
    final_deflection_b = min(deflection_b_input, deflection_b_equation)

    # Output deflection results
    print(f"lb: {lb:.2f}")
    print(f"ls: {ls:.2f}")
    print(f"std deflection conservative: {deflection_a_input:.2f}")
    print(f"std deflection conservative equation: {deflection_a_equation:.2f}")
    print(f"std deflection non-conservative: {deflection_b_input:.2f}")
    print(f"std deflection non-conservative equation: {deflection_b_equation:.2f}")
    print(f"d a: {final_deflection_a:.2f}")
    print(f"d b: {final_deflection_b:.2f}")

    # Final distance between sheathing is the minimum of all the constraints
    joist_dist = min(lb, ls, final_deflection_a, final_deflection_b)
    print(f"Final distance between joists: {joist_dist}")

    return no_of_spans, design_span, joist_dist, rolling_shear

def get_characteristics():
    """
    Function to gather nominal size and species information from the user.
    Returns the nominal size and thickness in inches.
    """
    # Input for nominal size
    input_nominal_size = input("Please enter nominal size: ")
    while input_nominal_size not in inch_options:
        input_nominal_size = input(f"Invalid option! Only {inch_options} are allowed. Please enter nominal size: ")

    # Input for species type
    species_nominal = input("Please choose between Douglas-Fir-Larch (1), Hem-Fir (2), Spruce-Pine-Fir (3): ")
    while species_nominal not in ["1", "2", "3"]:
        species_nominal = input("Invalid option! Please choose between Douglas-Fir-Larch (1), Hem-Fir (2), Spruce-Pine-Fir (3): ")

    # Input for species grade
    species_grade = input("Please choose species grade (1 or 2): ")
    while species_grade not in ["1", "2"]:
        species_grade = input("Invalid option! Only 1 or 2 are allowed. Please choose species grade: ")
    
    direction = input("Please choose X (1) or Y (2) direction: ")
    while direction not in ["1", "2"]:
        direction = input("Invalid option! Please choose X (1) or Y (2) direction: ")
    direction = "x" if direction == "1" else "y"

    # Displaying nominal values and selected species details
    print(f"Nominal Values: {big_table[input_nominal_size]}")
    i = big_table[input_nominal_size]["I" + direction]
    s = big_table[input_nominal_size]["S" + direction]

    species_nominal = species_nominal_mapper[species_nominal]
    shores_values = species_and_nominal_table[species_nominal + species_grade]
    print(f"Grade: {shores_values}")

    return input_nominal_size, i, s, shores_values

def calculate_joist_values(joist_s, joist_values, rolling_shear, weight_on_joists, no_of_spans, input_nominal_size):
    """
    Function to calculate joist-related values such as lb and ls, along with adjusted fb.
    """
    try:
        thickness, width = map(int, input_nominal_size.split("x"))
        fb_factor = adjustments_factor[width][thickness]
        fc_factor = adjustments_factor[thickness][2]  # Factor for compression (if needed)
    except:
        fb_factor = 1
        fc_factor = 1

    cd = 0.9  # Duration factor

    # Calculate new fb after adjustment
    new_fb = fb_factor * cd * joist_values["Fb"]

    # Calculate lb (based on bending stress)
    lb_constant = 120 if no_of_spans == 3 else 96
    joist_lb = ((lb_constant * new_fb * joist_s * 1e-9) / weight_on_joists) ** 0.5
    
    # Calculate ls based on span type
    if no_of_spans == 3:
        joist_ls = (20 * joist_values["Fv"] * rolling_shear * 1e-4) / weight_on_joists
    else:
        breadth, depth = map(float, inch_to_metric[input_nominal_size].split("*"))
        joist_ls = 16 * joist_values["Fv"] * breadth * depth * 1e-6 / 2 + 2 * depth * 1e-3
    
    return joist_lb, joist_ls

def calculate_deflections(joist_values, joist_i, weight_on_joists, no_of_spans):
    """
    Function to calculate deflections for joist spacing based on input parameters.
    """
    
    # Calculate deflections based on span type
    if no_of_spans == 3:
        deflection_360 = ((1743 * joist_values["E"] * joist_i) / (360 * weight_on_joists)) ** (1/3)
        deflection_16 = ((1743 * joist_values["E"] * joist_i) / (16 * weight_on_joists)) ** (1/4)
    else:
        deflection_360 = ((4608 * joist_values["E"] * joist_i) / (1800 * weight_on_joists)) ** (1/3)
        deflection_16 = ((4608 * joist_values["E"] * joist_i) / (80 * weight_on_joists)) ** (1/4)
    
    return deflection_360, deflection_16

def calculate_shores_values(shores_values, shores_i, shores_s, big_w, design_span, input_nominal_size):
    """
    Function to calculate shore-related values like lb, ls, and deflections.
    """
    # Calculate lb (shores distance based on bending stress)
    try:
        thickness, width = map(int, input_nominal_size.split("x"))
        fb_factor = adjustments_factor[width][thickness]
        fc_factor = adjustments_factor[thickness][2]  # Factor for compression (if needed)
    except:
        fb_factor = 1
        fc_factor = 1

    cd = 0.9  # Duration factor

    # Calculate new fb after adjustment
    new_fb = fb_factor * cd * shores_values["Fb"]
    shores_lb = ((120 * new_fb * shores_s * 1e-9) / big_w) ** 0.5

    # Calculate ls based on shores type
    breadth, depth = map(float, inch_to_metric[input_nominal_size].split("*"))
    shores_ls = ((192 * shores_values["Fv"] * breadth * depth * 1e-6) / (15 * big_w)) + (2 * depth * 1e-3)


    deflection_360 = ((1743 * shores_values["E"] * shores_i) / (360 * big_w)) ** (1/3)
    deflection_16 = ((1743 * shores_values["E"] * shores_i) / (16 * big_w)) ** (1/4)
    
    return shores_lb, shores_ls, deflection_360, deflection_16

def main():
    """
    Main function that orchestrates the calculation process by calling other helper functions.
    It calculates various structural values based on user input.
    """
    # Step 1: Calculate concrete weight plus live load
    concrete_weight_plus_live_load = get_concrete_weight()
    
    # Step 2: Get sheathing details
    is_plywood, ply_class, is_face_grain_across = get_sheathing_info()

    # Step 3: Get final sheathing thickness and related parameters
    sheathing_values, final_parameter, final_sheathing_weight = get_sheathing_thickness(is_plywood, ply_class, is_face_grain_across)
    
    # Step 4: Calculate distance between sheathing based on the input parameters
    no_of_spans, design_span, final_distance_between_sheathing, rolling_shear = get_sheathing_distance(sheathing_values, final_parameter, concrete_weight_plus_live_load, is_plywood)
    
    # Step 5: Get characteristics of nominal size and sheathing thickness
    input_nominal_size, joist_i, joist_s, joist_values = get_characteristics()

    weight_on_joists = concrete_weight_plus_live_load + final_sheathing_weight

    # Step 6: Calculate joist-related values and deflections
    joist_lb, joist_ls = calculate_joist_values(joist_s, joist_values, rolling_shear, weight_on_joists, no_of_spans, input_nominal_size)

    joist_i /= 1e12
    final_deflection_1, final_deflection_2 = calculate_deflections(joist_values, joist_i, weight_on_joists, no_of_spans)
    final_distance_between_joist = min(joist_lb, joist_ls, final_deflection_1, final_deflection_2)

    input_nominal_size, shores_i, shores_s, shores_values = get_characteristics()
    
    # Step 7: Calculate shore-related values and deflections
    shores_lb, shores_ls, final_deflection_i, final_deflection_ii = calculate_shores_values(shores_values, shores_i, shores_s, weight_on_joists, design_span, input_nominal_size)
    final_distance_between_shores = min(shores_lb, shores_ls, final_deflection_i, final_deflection_ii)

    # Step 8: Output final distances for sheathing, joist, and shores
    print()
    print(f"Final distance between joists: {final_distance_between_sheathing}")
    print(f"Final distance between stringers: {final_distance_between_joist}")
    print(f"Final distance between shores: {final_distance_between_shores}")

if __name__ == "__main__":
    main()  # Entry point for the program
