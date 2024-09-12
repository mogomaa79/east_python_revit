from utils import *
from bisect import bisect_right

def get_concrete_weight():
	# User input
	unit_weight_of_concrete = float(input("Please enter unit weight of concrete: "))
	thickness_of_slab = float(input("Please enter thickness of slab: "))
	suitable_live_load = float(input("Please enter suitable live load: "))
	is_motorized = input("Please choose Motorized (1) or non-motorized (2): ")

	# Validate motorized input
	while is_motorized not in ["1", "2"]:
		is_motorized = input("Invalid Option! Please choose Motorized (1) or Non-motorized (2): ")

	final_option = motorized_options if is_motorized == "1" else non_motorized_options

	# Calculate concrete weight
	concrete_weight = round(unit_weight_of_concrete * thickness_of_slab, 2)
	print(f"Concrete Weight: {concrete_weight}")

	# Calculate concrete weight plus live load
	concrete_weight_plus_live_load = concrete_weight + suitable_live_load
	print(f"Concrete Weight plus Live Load: {concrete_weight_plus_live_load}")

	# Determine final thickness
	final_thickness = thickness_options[bisect_right(thickness_options, thickness_of_slab)]
	print(f"Final Thickness: {final_thickness}")

	# Adjust concrete weight plus live load based on the final thickness option
	concrete_weight_plus_live_load = max(final_option[final_thickness], concrete_weight_plus_live_load)

	print(f"Final Concrete Weight plus Live Load: {concrete_weight_plus_live_load}\n")
	return concrete_weight_plus_live_load

def get_sheathing_info():
	plywood_or_plyform = input("Please choose between Plywood (1) and Plyform (2): ")
	while plywood_or_plyform not in ["1", "2"]:
		plywood_or_plyform = input("Invalid option! Please choose between Plywood (1) and Plyform (2): ")

	is_plywood = plywood_or_plyform == "1"

	if not is_plywood:
		ply_class = input("Please choose between Class I (1), Class II (2), Structural I (3): ")
		while ply_class not in ["1", "2", "3"]:
			ply_class = input("Invalid Option! Please choose between Class I (1), Class II (2), Structural I (3): ")
	else:
		ply_class = input("Please choose between Structural I and Marine (1), another class for different species(2): ")
		while ply_class not in ["1", "2"]:
			ply_class = input("Invalid Option! Please choose between Structural I and Marine (1), another class for different species(2): ")


	is_face_grain_across = input("Please choose between face grain across (1) or along (2): ")
	while is_face_grain_across not in ["1", "2"]:
		is_face_grain_across = input("Invalid Option! Please choose between face grain across (1) or along (2): ")
	
	print()
	return is_plywood, ply_class, is_face_grain_across

def get_sheathing_thickness(is_plywood, ply_class, is_face_grain_across):
	if not is_plywood:
		input_plyform_thickness = float(input("Please enter plyform thickness: "))
		while input_plyform_thickness not in plyform_thickness:
			print(f"Invalid option. Only {', '.join(map(str, plyform_thickness))} are allowed.")
			input_plyform_thickness = float(input("Please enter plyform thickness: "))

		final_sheathing_thickness = input_plyform_thickness
		final_sheathing_weight = plyform_weight_by_thickness[final_sheathing_thickness]

		final_parameter = plyform_general_mapper[f"{ply_class}_{is_face_grain_across}"][final_sheathing_thickness]

	elif ply_class == "2":
		input_species_thickness = float(input("Please enter different species thickness: "))
		while input_species_thickness not in different_species_thickness:
			print(f"Invalid option. Only {', '.join(map(str, different_species_thickness))} are allowed.")
			input_species_thickness = float(input("Please enter different species thickness: "))

		final_sheathing_thickness = input_species_thickness
		final_sheathing_weight = plywood_weight_different[final_sheathing_thickness]
		final_parameter = plywood_across_different[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_different[final_sheathing_thickness]

	elif ply_class == "1":
		input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
		while input_structural_marine_thickness not in structural_marine_thickness:
			print(f"Invalid option. Only {', '.join(map(str, structural_marine_thickness))} are allowed.")
			input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
		final_sheathing_thickness = input_structural_marine_thickness
		final_sheathing_weight = plywood_weight_marine[final_sheathing_thickness]
		final_parameter = plywood_across_marine[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_marine[final_sheathing_thickness]

	print(f"Final Sheathing Thickness: {final_sheathing_thickness}")
	print(f"Final Sheathing Weight: {final_sheathing_weight}")
	print(f"Final Parameters: {final_parameter}\n")

	final_values = {}
	if is_plywood:
		stress_group = int(input("Please choose stress group of plywood (1-6): "))
		while stress_group not in range(1, 7): 
			stress_group = int(input("Invalid option! Please choose stress group of plywood (1-6): "))

		final_stress = stress_of_plywood
		stress_grade_level = input("Please choose stress grade level S-1, 2, or 3: ")
		while stress_grade_level not in ["1", "2", "3"]:
			stress_grade_level = input("Invalid option! Please choose stress grade level S-1, 2, or 3: ")

		if stress_grade_level in ["1", "2"]:
			is_wet = input("Is it wet (1) or dry (2)? ")
			while is_wet not in ["1", "2"]:
				is_wet = input("Invalid option! Is it wet (1) or dry (2)? ")
			index = 0 if stress_grade_level == "1" and is_wet == "1" else 1 if stress_grade_level == "1" and is_wet == "2" else 2 if stress_grade_level == "2" and is_wet == "1" else 3
		else:
			is_wet = "2"
			index = 4

		for k, v in final_stress.items():
			if stress_group in v:
				final_values[k] = v[stress_group][index]

	else:
		final_values = plyform_stress[str(ply_class)]

	print("Final Values:")
	for k, v in final_values.items():
		print(f"{k}: {v}")

	return final_values, final_parameter

def get_sheathing_distance(final_values, final_parameter, concrete_weight_plus_live_load, is_plywood):
    no_of_spans = input("Please enter number of spans (1-3): ")
    while no_of_spans not in ["1", "2", "3"]:
        no_of_spans = input("Invalid option! Please enter number of spans (1-3): ")

    no_of_spans = int(no_of_spans)

    # Bending stress
    fb = final_values["Fb"]
    fs = final_values["Fs"]
    E = final_values["E"]

    print(f"fb: {fb}")
    
    se_index = 2 if is_plywood else 1
    final_parameter_se = final_parameter[se_index]
    print(f"se: {final_parameter_se}")
    print(f"wb: {concrete_weight_plus_live_load}")
    
    print(f"fs: {fs}")
    print(f"E: {E}")
    
    i_index = 1 if is_plywood else 0
    final_parameter_i = final_parameter[i_index]
    print(f"I: {final_parameter_i}")

    design_span = float(input("Enter design span (m): ")) * 1000

    lb_constant = 120 if no_of_spans == 3 else 96
    lb = (((lb_constant * fb * final_parameter_se) / concrete_weight_plus_live_load) ** 0.5) / 1000 

    ls = (ls_constant_mapper[no_of_spans] * fs * final_parameter_se) / (concrete_weight_plus_live_load * 1000)

    deflection_a_input = design_span / 360
    deflection_b_input = design_span / 16
    deflection_a_equation = ((1743 * E * final_parameter_i) / (360 * concrete_weight_plus_live_load)) ** (1/3)
    deflection_b_equation = ((1743 * E * final_parameter_i) / (16 * concrete_weight_plus_live_load)) ** (1/4)
    final_deflection_a = min(deflection_a_input, deflection_a_equation)
    final_deflection_b = min(deflection_b_input, deflection_b_equation)

    print(f"lb: {lb}")
    print(f"ls: {ls} OOM FASH5")
    print(f"std deflection conservative: {deflection_a_input}")
    print(f"std deflection conservative equation: {deflection_a_equation}")
    print(f"std deflection non-conservative: {deflection_b_input}")
    print(f"std deflection non-conservative equation: {deflection_b_equation}")
    print(f"d a: {final_deflection_a}")
    print(f"d b: {final_deflection_b}")

    final_distance_between_sheathing = min(lb, ls, final_deflection_a, final_deflection_b)
    print(f"Final distance between sheathing: {final_distance_between_sheathing}")

    return no_of_spans, design_span, final_distance_between_sheathing, final_parameter_i, final_parameter_se

def get_characteristics():
	input_nominal_size = input("Please enter nominal size: ")
	while input_nominal_size not in inch_options:
		input_nominal_size = input(f"Invalid option! Only {inch_options} are allowed. Please enter nominal size: ")

	species_nominal = input("Please choose between Douglas-Fir-Larch (1), Hem-Fir (2), Spruce-Pine-Fir (3): ")
	while species_nominal not in ["1", "2", "3"]:
		species_nominal = input("Invalid option! Please choose between Douglas-Fir-Larch (1), Hem-Fir (2), Spruce-Pine-Fir (3): ")

	species_grade = input("Please choose species grade (1 or 2): ")
	while species_grade not in ["1", "2"]:
		species_grade = input("Invalid option! Only 1 or 2 are allowed. Please choose species grade: ")

	print(f"Nominal Values: {big_table[input_nominal_size]}")
	species_nominal = species_nominal_mapper[species_nominal]
	print(f"Grade: {species_and_nominal_table[species_nominal + species_grade]}")
    
	inch_thickness = input("Please enter sheathing thickness in inches (2, 3, or 4): ")
	while inch_thickness not in ["2", "3", "4"]:
		inch_thickness = input("Invalid Option! Please enter sheathing thickness in inches (2, 3, or 4): ")

	return input_nominal_size, inch_thickness

def calculate_joist_values(final_values, final_parameter_se, concrete_weight_plus_live_load, no_of_spans, inch_thickness, input_nominal_size):
    fb_index = 1 if inch_thickness == '4' else 0
    inches = int(input_nominal_size.split("x")[0])
    fb_factor = adjustments_factor[inches][fb_index]
    fc_factor = adjustments_factor[inches][2] # CHECK THIS IF NEEDED
    cd = 0.9
    new_fb = fb_factor * cd * final_values["Fb"]

    lb_constant = 120 if no_of_spans == 3 else 96
    joist_lb = ((lb_constant * new_fb * final_parameter_se) / concrete_weight_plus_live_load) ** 0.5
    
    if no_of_spans == 3:
        joist_ls = (20 * final_values["Fs"] * final_parameter_se) / concrete_weight_plus_live_load
    else:
        breadth = float(inch_to_metric[input_nominal_size].split("*")[0])
        depth = float(inch_to_metric[input_nominal_size].split("*")[0])
        joist_ls = ((16 * final_values["Fs"] * breadth * depth) / 2) + (2 * depth)
    
    return joist_lb, joist_ls, new_fb

def calculate_deflections(final_values, final_parameter_i, concrete_weight_plus_live_load, design_span, no_of_spans):
    deflection_1_input = design_span / 360
    deflection_2_input = design_span / 16

    if no_of_spans == 3:
        deflection_1_equation = ((1743 * final_values["E"] * final_parameter_i) / (360 * concrete_weight_plus_live_load)) ** (1/3)
        deflection_2_equation = ((1743 * final_values["E"] * final_parameter_i) / (16 * concrete_weight_plus_live_load)) ** (1/4)
    else:
        deflection_1_equation = ((4608 * final_values["E"] * final_parameter_i) / (1800 * concrete_weight_plus_live_load)) ** (1/3)
        deflection_2_equation = ((4608 * final_values["E"] * final_parameter_i) / (80 * concrete_weight_plus_live_load)) ** (1/4)

    final_deflection_1 = min(deflection_1_input, deflection_1_equation)
    final_deflection_2 = min(deflection_2_input, deflection_2_equation)
    
    return final_deflection_1, final_deflection_2

def calculate_shores_values(final_values, final_parameter_i, final_parameter_se, big_w, design_span, input_nominal_size, new_fb):
    shores_lb = ((120 * new_fb * final_parameter_se) / big_w) ** 0.5

    breadth, depth= map(float, inch_to_metric[input_nominal_size].split("*"))

    shores_ls = ((192 * final_values["Fs"] * breadth * depth) / (15 * big_w)) + (2 * depth)

    deflection_i_input = design_span / 360
    deflection_ii_input = design_span / 16
    deflection_i_equation = ((1743 * final_values["E"] * final_parameter_i) / (360 * big_w)) ** (1/3)
    deflection_ii_equation = ((1743 * final_values["E"] * final_parameter_i) / (16 * big_w)) ** (1/4)

    final_deflection_i = min(deflection_i_input, deflection_i_equation)
    final_deflection_ii = min(deflection_ii_input, deflection_ii_equation)
    
    return shores_lb, shores_ls, final_deflection_i, final_deflection_ii

def main():
	concrete_weight_plus_live_load = get_concrete_weight()
	
	is_plywood, ply_class, is_face_grain_across = get_sheathing_info()

	final_values, final_parameter = get_sheathing_thickness(is_plywood, ply_class, is_face_grain_across)
	
	no_of_spans, design_span, final_distance_between_sheathing, final_parameter_i, final_parameter_se = get_sheathing_distance(final_values, final_parameter, concrete_weight_plus_live_load, is_plywood)
	
	input_nominal_size, inch_thickness = get_characteristics()

	joist_lb, joist_ls, new_fb = calculate_joist_values(final_values, final_parameter_i, concrete_weight_plus_live_load, no_of_spans, inch_thickness, input_nominal_size)	
	final_deflection_1, final_deflection_2 = calculate_deflections(final_values, final_parameter_i, concrete_weight_plus_live_load, design_span, no_of_spans)
	final_distance_between_joist = min(joist_lb, joist_ls, final_deflection_1, final_deflection_2)

	shores_lb, shores_ls, final_deflection_i, final_deflection_ii = calculate_shores_values(final_values, final_parameter_i, final_parameter_se, concrete_weight_plus_live_load, design_span, input_nominal_size, new_fb)
	final_distance_between_shores = min(shores_lb, shores_ls, final_deflection_i, final_deflection_ii)

	print()
	print(f"Final distance between sheathing: {final_distance_between_sheathing}")
	print(f"Final distance between joists: {final_distance_between_joist}")
	print(f"Final distance between shores: {final_distance_between_shores}")

if __name__ == "__main__":
	main()