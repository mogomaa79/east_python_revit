from utils import *
from bisect import bisect_right

unit_weight_of_concrete = float(input("Please enter unit weight of concrete: "))
thickness_of_slab = float(input("Please enter thickness of slab: "))
suitable_live_load = float(input("Please enter suitable live load: "))
is_motorized = input("Please choose motorized(1) or not motorized(2): ")

while str(is_motorized) not in ["1", "2"]:
	print("Invalid option only 1 or 2 allowed")
	is_motorized = input("Please choose motorized(1) or not motorized(2): ")

is_motorized = is_motorized == "1"
final_option = motorized_options if is_motorized else non_motorized_options

concrete_weight = round(unit_weight_of_concrete * thickness_of_slab, 2)
print("concrete Weight: {}".format(concrete_weight))

concrete_weight_plus_live_load = concrete_weight + float(suitable_live_load)
print("concrete Weight plus Live Load: {}".format(concrete_weight_plus_live_load))

final_thickness = thickness_options[bisect_right(thickness_options, thickness_of_slab)]
print("Final Thickness: {}".format(final_thickness))

if concrete_weight_plus_live_load < final_option[final_thickness]:
	concrete_weight_plus_live_load = final_option[final_thickness]

print("Final concrete Weight plus Live Load: {}".format(concrete_weight_plus_live_load))

plywood_or_plyform = input("Please choose between plywood(1) and plyform(2): ")
while str(plywood_or_plyform) not in ["1", "2"]:
	print("Invalid option only 1 or 2 allowed")
	plywood_or_plyform = input("Please choose between plywood(1) and plyform(2): ")

is_plywood = plywood_or_plyform == "1"

if not is_plywood:
	ply_class = input("Please choose between Class I(1), Class II(2), Structural I(3): ")
	while str(ply_class) not in ["1", "2", "3"]:
		print("Invalid option only 1 or 2 or 3 allowed")
		ply_class = input("Please choose between Class I(1), Class II(2), Structural I(3): ")
else:
	ply_class = input("Please choose between Structural I and Marine (1), another class for different species(2): ")
	while str(ply_class) not in ["1", "2"]:
		print("Invalid option only 1 or 2  allowed")
		ply_class = input("Please choose between Structural I and Marine (1), another class for different species(2): ")


is_face_grain_across = input("Please choose is face grain across(1) or along(2): ")

if not is_plywood:
	input_plyform_thickness = float(input("Please enter plyform thickness: "))
	while input_plyform_thickness not in plyform_thickness:
		print("Invalid option only {} are allowed".format(str(plyform_thickness)))
		input_plyform_thickness = float(input("Please enter plyform thickness: "))
	final_sheathing_thickness = input_plyform_thickness
	final_sheathing_weight = plyform_weight_by_thickness[final_sheathing_thickness]
	final_parameter = plyform_general_mapper[ply_class + "_" + is_face_grain_across][final_sheathing_thickness]

elif ply_class == "2":
	input_species_thickness = float(input("Please enter different species thickness: "))
	while input_species_thickness not in different_species_thickness:
		print("Invalid option only {} are allowed".format(str(different_species_thickness)))
		input_species_thickness = float(input("Please enter different species thickness: "))
	final_sheathing_thickness = input_species_thickness
	final_sheathing_weight = plywood_weight_different[final_sheathing_thickness]
	final_parameter = plywood_across_different[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_different[final_sheathing_thickness]
elif ply_class == "1":
	input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
	while input_structural_marine_thickness not in structural_marine_thickness:
		print("Invalid option only {} are allowed".format(str(structural_marine_thickness)))
		input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
	final_sheathing_thickness = input_structural_marine_thickness
	final_sheathing_weight = plywood_weight_marine[final_sheathing_thickness]
	final_parameter = plywood_across_marine[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_marine[final_sheathing_thickness]

print("Final Sheathing Thickness: {}".format(final_sheathing_thickness))
print("Final sheathing weight: {}".format(final_sheathing_weight))
print("Final paramteres: {}".format(final_parameter)) 

final_values = {}
if is_plywood:
	stress_group = int(input("Please choose stress group of plywood 1, 2, 3, 4, Marine and Structural I (5), All Others (6): "))
	final_stress = stress_of_plywood
	stress_grade_level = input("Please choose stress grade level S- 1, 2, 3: ")
	if stress_grade_level in ["1", "2"]:
		is_wet = input("Please choose is wet(1), or dry(2): ")
		if stress_grade_level == "1":
			index = 0 if is_wet == "1" else 1
		else:
			index = 2 if is_wet == "1" else 3
	else:
		is_wet = "2"
		index = 4
	for k, v in final_stress.items():
		if stress_group in v.keys():
			final_values[k] = v[stress_group][index]
else:
	final_values = plyform_stress[str(ply_class)]

print("Final values: ")
for k, v in final_values.items():
	print(k, v, sep=": ")


no_of_spans = str(input("Please enter number of spans: "))
while no_of_spans not in ["1", "2", "3"]:
	print("Invalid option only 1 or 2 or 3 are allowed")
	no_of_spans = str(input("Please enter number of spans: "))

no_of_spans = int(no_of_spans)

#bending stress
final_values_fb = final_values["Fb"]
print("fb: {}".format(final_values["Fb"]) )

se_index = 2 if is_plywood else 1
final_parameter_se = final_parameter[se_index]
print("se: {}".format(final_parameter[se_index]))
print("wb: {}".format(concrete_weight_plus_live_load))

final_values_fs = final_values["Fs"]
print("fs: {}".format(final_values["Fs"]) )

final_values_e = final_values["E"]
print("E: {}".format(final_values["E"]) )

i_index = 1 if is_plywood else 0
final_parameter_i = final_parameter[i_index]
print("I: {}".format(final_parameter[i_index]))

design_span = float(input("Enter design span (m): ")) * 1000

lb_constant = 120 if no_of_spans == 3 else 96
lb = (( (lb_constant * final_values_fb * final_parameter_se) / concrete_weight_plus_live_load) ** 0.5) / 1000 

print(f"fs {final_values_fs}, se {final_parameter_se}")
ls = (ls_constant_mapper[no_of_spans] * final_values_fs * final_parameter_se) / (concrete_weight_plus_live_load * 1000) # !!!! check this

deflection_a_input = design_span / 360
deflection_b_input = design_span / 16
deflection_a_equation = ((1743 * final_values_e * final_parameter_i) / (360 * concrete_weight_plus_live_load)) ** (1/3)
deflection_b_equation = ((1743 * final_values_e * final_parameter_i) / (16 * concrete_weight_plus_live_load)) ** (1/4)
final_deflection_a = min(deflection_a_input, deflection_a_equation)
final_deflection_b = min(deflection_b_input, deflection_b_equation)

print("lb: {}".format(lb))
print("ls: {} OOM FASH5".format(ls))
print(f"std deflection conservative {deflection_a_input}")
print(f"std deflection conservative equation {deflection_a_equation}")
print(f"std deflection non-conservative {deflection_b_input}")
print(f"std deflection non-conservative equation {deflection_b_equation}")
print("d a: {}".format(final_deflection_a))
print("d b: {}".format(final_deflection_b))

final_distance_between_sheathing = min(lb, ls, final_deflection_a, final_deflection_b)
print("Final distance between sheathing: {}".format(final_distance_between_sheathing))

input_nominal_size = input("Please enter nominal size: ")
while input_nominal_size not in inch_options:
	print("Invalid option only {} are allowed".format(str(inch_options)))
	input_nominal_size = input("Please enter nominal size: ")

print("nominal values: {}".format(big_table[input_nominal_size]))

species_nominal = str(input("Please choose between Douglas-Fir-Larch(1), Hem-Fir (2), Spruce-Pine-Fir (3): "))
while species_nominal not in ["1", "2", "3"]:
	print("Invalid option only 1 or 2 or 3 allowed")
	species_nominal = str(input("Please choose between Douglas-Fir-Larch(1), Hem-Fir (2), Spruce-Pine-Fir (3): "))

species_nominal = species_nominal_mapper[species_nominal]

species_grade = str(input("Please choose species grade: "))
while species_grade not in ["1", "2"]:
	print("Invalid option only 1 or 2 allowed")
	species_grade = str(input("Please choose species grade: "))

print("grade: {}".format(species_and_nominal_table[species_nominal + species_grade]))


inch_thickness = input("Please enter sheathing thickness in inches: ")
while inch_thickness not in ["2", "3", "4"]:
	print("Invalid option only 2 or 3 or 4 are allowed")
	inch_thickness = input("Please enter sheathing thickness in inches: ")

fb_index = 1 if inch_thickness == '4' else 1
inches = int(input_nominal_size.split("x")[0]) # COULD BE TAKEN AS INPUT (CHECK DICTIONARY)
fb_factor = adjustments_factor[inches][fb_index]
fc_factor = adjustments_factor[inches][2]
cd = 0.9

new_fb = fb_factor * cd * final_values_fb

lb_constant = 120 if no_of_spans == 3 else 96
jois_lb = ( (lb_constant * new_fb * final_parameter_se) / concrete_weight_plus_live_load) ** 0.5 # CHECK THIS


if no_of_spans == 3:
	joist_ls = (20 * final_values_fs * final_parameter_se) / concrete_weight_plus_live_load # CHECK THIS
else:
	breadth = float(inch_to_metric[input_nominal_size].split("*")[0] )
	depth = float(inch_to_metric[input_nominal_size].split("*")[0] )
	joist_ls = ((16 * final_values_fs * breadth * depth) / 2) + (2 * depth)

deflection_1_input = design_span / 360
deflection_2_input = design_span / 16
if no_of_spans == 3:
	deflection_1_equation = ((1743 * final_values_e * final_parameter_i) / (360 * concrete_weight_plus_live_load)) ** (1/3)
	deflection_2_equation = ((1743 * final_values_e * final_parameter_i) / (16 * concrete_weight_plus_live_load)) ** (1/4)
else:
	deflection_1_equation = ((4608 * final_values_e * final_parameter_i) / (1800 * concrete_weight_plus_live_load)) ** (1/3)
	deflection_2_equation = ((4608 * final_values_e * final_parameter_i) / (80 * concrete_weight_plus_live_load)) ** (1/4)
final_deflection_1 = deflection_1_input if deflection_1_input < deflection_1_equation else deflection_1_equation
final_deflection_2 = deflection_2_input if deflection_2_input < deflection_2_equation else deflection_2_equation

final_distance_between_joist = min(jois_lb, joist_ls, final_deflection_1, final_deflection_2)

big_w = concrete_weight_plus_live_load # CHECK THIS

shores_lb = ( (120 * new_fb * final_parameter_se) / big_w) ** 0.5
breadth = float(inch_to_metric[input_nominal_size].split("*")[0] )
depth = float(inch_to_metric[input_nominal_size].split("*")[0] )
shores_ls = ((192 * final_values_fs * breadth * depth) / (15 * big_w)) + (2 * depth)
deflection_i_input = design_span / 360
deflection_ii_input = design_span / 16
deflection_i_equation = ((1743 * final_values_e * final_parameter_i) / (360 * big_w)) ** (1/3)
deflection_ii_equation = ((1743 * final_values_e * final_parameter_i) / (16 * big_w)) ** (1/4)
final_deflection_i = deflection_i_input if deflection_i_input < deflection_i_equation else deflection_i_equation
final_deflection_ii = deflection_ii_input if deflection_ii_input < deflection_ii_equation else deflection_ii_equation

final_distance_between_shores = min(shores_lb, shores_ls, final_deflection_i, final_deflection_ii)
 

print("final distance sheathing: {}".format(final_distance_between_sheathing))
print("final distance joists: {}".format(final_distance_between_joist))
print("final distance shores: {}".format(final_distance_between_shores))
