#yehia phd
from bisect import bisect_right

non_motorized_optinos = {
	0.10: 4.8,
	0.13: 5.4,
	0.15: 6.0,
	0.18: 6.6,
	0.20: 7.2,
	0.23: 7.8,
	0.25: 8.4,
	0.30: 9.6,
	}


motorized_options = {
	0.10: 6.0,
	0.13: 6.6,
	0.15: 7.2,
	0.18: 7.8,
	0.20: 8.4,
	0.23: 9.0,
	0.25: 9.6,
	0.30: 10.8,
	}


thickness_options = [0, 0.10,0.13,0.15,0.18,0.20,0.23,0.25,0.30, 1]

unit_weight_of_concrete = float(input("Please enter unit weight of concrete: "))
thickness_of_slab = float(input("Please enter thickness of slab: "))
suitable_live_load = float(input("Please enter suitable live load: "))
is_motorized = input("Please choose motorized(1) or not motorized(2): ")

while str(is_motorized) not in ["1", "2"]:
	print("Invalid option only 1 or 2 allowed")
	is_motorized = input("Please choose motorized(1) or not motorized(2): ")

is_motorized = is_motorized == "1"
final_option = motorized_options if is_motorized else non_motorized_optinos

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

plyflorm_thickness = [11.9,12.7,15.1,15.9,18.25,19.05,22.22,25.4,28.6,]
different_species = [6.78,7.32,10.80,13.97,14.43,14.88,20.75,21.23,]
structural_marine = [8.69,9.47,13.84,18.21,19.00,19.76,27.71,28.47,]



plyform_appx_weight = {
11.9: 0.07,
12.7: 0.07,
15.1: 0.08,
15.9: 0.09,
18.25: 0.10,
19.05: 0.11,
22.22: 0.12,
25.4: 0.14,
28.6: 0.16,
}

plyform_across_class_1 = {11.9:[8372.8,1218.9,932.6],
12.7:[9768.3,1338.8,1013.3],
15.1:[14589,1673.5,1069.3],
15.9:[16491.9,1788.4,1124.2],
18.25:[22835,2148,1378.2],
19.05:[25245.4,2272.9,1413.2],
22.22:[37550.9,2917.3,1682.2],
25.4:[54169.7,3681.6,1843.3],
28.6:[70281.1,4241.1,2050.9],
}

plyform_across_class_2 = {11.9:[7992.3,1213.9,884.7],
12.7:[9514.6,1333.8,961.7],
15.1:[14589,1668.5,1047.3],
15.9:[16491.9,1783.4,1099.8],
18.25:[22835,2148,1278.9],
19.05:[25118.5,2267.9,1303.9],
22.22:[38058.3,2952.3,1571.1],
25.4:[53408.5,3766.6,1693.8],
28.6:[71803.4,4341,1882],}


plyform_across_structural_1 = {11.9:[8499.7,1228.9,885.4],
12.7:[9895.2,1353.8,965.1],
15.1:[14715.9,1688.5,986.7],
15.9:[16618.8,1803.3,1033.9],
18.25:[23215.6,2193,1201.2],
19.05:[25626,2317.9,1217],
22.22:[40215,3127.1,1482.4],
25.4:[60766.5,4131.2,1568.8],
28.6:[79034.5,4770.6,1738.5],
}


plyform_along_class_1 = {11.9:[2283.5,534.5,475.7],
12.7:[3044.7,649.4,538.6],
15.1:[3679,729.3,557.3],
15.9:[4820.7,874.2,608.4],
18.25:[9134,1233.9,746.8],
19.05:[11671.2,1528.6,798.9],
22.22:[19156,2108.1,1185.3],
25.4:[34252.5,3167.1,1379.2],
28.6:[50490.7,3991.3,1655.5],
}

plyform_along_class_2 = {11.9:[1902.9,689.4,478.6],
12.7:[2537.2,834.2,536.2],
15.1:[3171.5,939.1,552.9],
15.9:[4059.6,1124,604.5],
18.25:[7611.7,1583.6,743.5],
19.05:[9514.6,1958.2,796.2],
22.22:[15603.9,2707.5,1179.2],
25.4:[27909.5,4056.3,1373.9],
28.6:[40976.2,5110.3,1649.4],
}

plyform_along_structural_1 = {11.9:[2664.1,734.3,472.9],
12.7:[3679,889.2,535.8],
15.1:[4313.3,994.1,552.7],
15.9:[5708.8,1188.9,604.3],
18.25:[10783.2,1688.5,743.3],
19.05:[13701,2088.1,795.8],
22.22:[22708.1,2892.4,1178],
25.4:[40722.4,4346,1372.7],
28.6:[60132.2,5485,1647.2],}


plyform_general_mapper = {
	"1_1": plyform_across_class_1,
	"2_1": plyform_across_class_2,
	"3_1": plyform_across_structural_1,
	"1_2": plyform_along_class_1,
	"2_2": plyform_along_class_2,
	"3_2": plyform_along_structural_1
}


plywood_weight_different = {6.78:0.038,
7.32:0.053,
10.8:0.072,
13.97:0.086,
14.43:0.105,
14.88:0.124,
20.75:0.144,
21.23:0.158,}

plywood_weight_maring = {8.69:0.038,
9.47:0.053,
13.84:0.072,
18.21:0.086,
19:0.105,
19.76:0.124,
27.71:0.144,
28.47:0.158,}


plywood_across_different = {6.78:[195.8,1014.9,294.7,395.2],
7.32:[257,3425.3,624.4,607.2],
10.8:[382.8,9768.3,1178.9,878.2],
13.97:[486.7,16365.1,1693.5,1145.2],
14.43:[567.1,24991.6,2058.1,1329.6],
14.88:[578.5,35267.4,2572.6,1582.9],
20.75:[731.7,53662.3,3317,1746.5],
21.23:[757.8,69519.9,4096.3,1943.3],}

plywood_across_marin = {8.69:[251.7,1522.3,414.6,395],
9.47:[330.3,4820.7,884.2,606.8],
13.84:[382.8,9895.2,1353.8,876.4],
18.21:[611.9,16618.8,1803.3,1166.8],
19:[756.7,25626,2317.9,1217],
19.76:[777.1,36536,2842.4,1482.4],
27.71:[1025.5,60766.5,4131.2,1568.8],
28.47:[1099.8,79034.5,4770.6,1738.5],}



plywood_along_different = {6.78:[68.4,126.9,45,397],
7.32:[123.1,253.7,114.9,690.2],
10.8:[243.8,1141.8,434.6,541.1],
13.97:[300.5,3425.3,819.3,613.3],
14.43:[409.2,7992.3,1423.7,802.1],
14.88:[521.3,13193.6,1968.2,998.5],
20.75:[622,23469.3,2952.3,1382.5],
21.23:[625.3,34379.4,3716.6,1657.2],}

plywood_along_marin = {8.69:[123.1,126.9,64.9,535.4],
9.47:[221.4,253.7,164.8,968.8],
13.84:[438.9,1776.1,614.4,535.8],
18.21:[540.9,5708.8,1188.9,604.3],
19:[736.4,13701,2088.1,795.8],
19.76:[938.3,22708.1,2892.4,992.2],
27.71:[1119.4,40722.4,4346,1372.7],
28.47:[1125.5,60132.2,5485,1647.2],}


is_face_grain_across = input("Please choose is face grain across(1) or along(2): ")

if not is_plywood:
	input_plyform_thickness = float(input("Please enter plyform thickness: "))
	while input_plyform_thickness not in plyflorm_thickness:
		print("Invalid option only {} are allowed".format(str(plyflorm_thickness)))
		input_plyform_thickness = float(input("Please enter plyform thickness: "))
	final_sheathing_thickness = input_plyform_thickness
	final_sheathing_weight = plyform_appx_weight[final_sheathing_thickness]
	final_parameter = plyform_general_mapper[ply_class + "_" + is_face_grain_across][final_sheathing_thickness]

elif ply_class == "2":
	input_species_thickness = float(input("Please enter different species thickness: "))
	while input_species_thickness not in different_species:
		print("Invalid option only {} are allowed".format(str(different_species)))
		input_species_thickness = float(input("Please enter different species thickness: "))
	final_sheathing_thickness = input_species_thickness
	final_sheathing_weight = plywood_weight_different[final_sheathing_thickness]
	final_parameter = plywood_across_different[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_different[final_sheathing_thickness]
elif ply_class == "1":
	input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
	while input_structural_marine_thickness not in structural_marine:
		print("Invalid option only {} are allowed".format(str(structural_marine)))
		input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
	final_sheathing_thickness = input_structural_marine_thickness
	final_sheathing_weight = plywood_weight_maring[final_sheathing_thickness]
	final_parameter = plywood_across_marin[final_sheathing_thickness] if is_face_grain_across == "1" else plywood_along_marin[final_sheathing_thickness]

print("Final Sheathing Thickness: {}".format(final_sheathing_thickness))
print("Final sheathing weight: {}".format(final_sheathing_weight))
print("Final paramteres: {}".format(final_parameter)) 


stess_of_plywood = {
	"Fb": {
		1: [68.4684, 95.76, 56.9772, 79.002, 79.002],
		2: [46.9224, 67.032, 39.2616, 57.456, 57.456],
		3: [46.9224, 67.032, 39.2616, 57.456, 57.456],
		4: [45.0072, 63.6804, 37.3464, 53.1468, 53.1468],
	},
	"fc": {
		1: [46.4436, 78.5232, 43.092, 73.7352, 73.7352],
		2: [34.9524, 57.456, 32.5584, 52.668, 52.668],
		3: [29.2068, 50.7528, 27.7704, 45.486, 45.486],
		4: [29.2068, 47.88, 27.7704, 45.486, 45.486],
	},
	"Fs": {
		1: [7.4214, 9.0972, 7.4214, 9.0972, 7.6608],
		2: [5.7456, 6.7032, 5.7456, 6.7032, 5.7456],
		3: [5.7456, 6.7032, 5.7456, 6.7032, 5.7456],
		4: [5.2668, 6.2244, 5.2668, 6.2244, 5.5062],
	},
	"g": {
		1: [3351.6, 4309.2, 3351.6, 4309.2, 3926.16],
		2: [2872.8, 3591, 2872.8, 3591, 3255.84],
		3: [2394, 2872.8, 2394, 2872.8, 2633.4],
		4: [2154.6, 2394, 2154.6, 2394, 2154.6],
	},
	"fcper": {
		1: [10.0548, 16.2792, 10.0548, 16.2792, 16.2792],
		2: [6.4638, 10.0548, 6.4638, 10.0548, 10.0548],
		3: [6.4638, 10.0548, 6.4638, 10.0548, 10.0548],
		4: [5.0274, 7.6608, 5.0274, 7.6608, 7.6608],
	},
	"E": {
		1: [71820, 86184, 71820, 86184, 86184],
		2: [62244, 71820, 62244, 71820, 71820],
		3: [52668, 57456, 52668, 57456, 57456],
		4: [43092, 47880, 43092, 47880, 47880],
	},
	"Fss": {
		5: [3.01644, 3.591, 3.01644, 3.591, 0],
		6: [2.10672, 2.53764, 2.10672, 2.53764, 2.29824],
	}
}


plyform_stress = {
	"1": {
		"Fb": 13306.89,
		"Fs": 496.42,
		"E": 11376354,
		"Ee": 10342140,
	},
	"2": {
		"Fb": 9170.03,
		"Fs": 496.42,
		"E": 9859506.8,
		"Ee": 8963188,
	},
	"3": {
		"Fb": 13306.89,
		"Fs": 703.27,
		"E": 11376354,
		"Ee": 10342140,
	}
}






final_values = {}
if is_plywood:
	stress_group = int(input("Please choose stress group of plywood 1, 2, 3, 4, Marine and Structural I (5), All Others (6): "))
	final_stress = stess_of_plywood
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

ls_constant_mapper = {
	1: 24,
	2: 19.2,
	3: 20,
}

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

# Net Area, Ix, Sx, Iy, Sy
big_table = {"1x4": [66.548,1115500.222,25076.7,51196.4654,5375.92],
"1x6": [104.648,4328806.83,61954.2,80332.66522,8457.24],
"1x8": [137.922,9914632.567,107682.3,106139.0136,11145.2],
"1x10": [176.022,20590968.64,175373,135275.2135,14210.13],
"1x12": [214.122,37040434.6,259289.8,164827.6447,17291.45],
"2x4": [133.35,2231000.443,501531.4,409571.7232,21520.07],
"2x6": [209.55,8657613.661,123908.4,643910.016,33812.57],
"2x8": [276.098,19825102.82,215364.6,848695.8776,44564.41],
"2x10": [352.298,41177774.97,350582.1,1083450.402,56856.91],
"2x12": [428.498,74076706.89,518579.6,1316956.232,69149.41],
"3x4": [222.25,3716946.634,83589,1898015.303,59823.5],
"3x6": [349.25,14426581.23,206514,2980217.01,93914.7],
"3x8": [460.248,33044612.91,358941,3929224.661,123744.5],
"3x10": [587.248,68628237.52,584303.5,5011426.369,157999.6],
"3x12": [714.248,123466727.9,864244.7,6097790.391,192090.8],
"4x4": [311.15,5202892.825,117188.5,5207055.139,117188.5],
"4x6": [488.95,20199711.1,289283.5,8178947.521,184059.7],
"4x8": [644.652,46259960.69,502517.4,10780393.93,242572],
"4x10": [822.198,96082862.38,818024.9,13756448.63,309607.1],
"4x12": [999.998,172852586.6,1210073.7,16732503.33,376478.3],
"5x5": [514.35,14222627.83,248964.1,14222627.83,248964.1],
"6x6": [768.35,31737646.23,454494.7,31741808.55,454494.7],
"6x8": [1047.75,80478346.22,845068.4,43279743.68,619705.9],
"6x10": [1327.15,163978532.6,1355944.7,54821841.12,785081],
"6x12": [1606.55,290138277.8,1986468,66363938.56,950292.2],
"8x8": [1428.75,109760227,1152380.9,109747740.1,1152380.9],
"8x10": [1809.75,223058421.2,1848792,139012971.7,1459693.4],
"8x12": [2190.75,395627970.4,2709267,168278203.2,1767005.9],
"10x10": [2292.35,282537892,2342131,282517080.4,2342131],
"10x12": [2774.95,501142636.9,3432066,341996551.2,2851532.2],
"12x12": [3359.15,606657303.4,4154865,606657303.4,4154537.2],
}

inch_to_metric = {"1x4": "19.05*88.9",
"1x6": "19.05*139.7",
"1x8": "19.05*184.15",
"1x10": "19.05*234.95",
"1x12": "19.05*285.75",
"2x4": "38.1*88.9",
"2x6": "38.1*139.7",
"2x8": "38.1*184.15",
"2x10": "38.1*234.95",
"2x12": "38.1*285.75",
"3x4": "63.5*88.9",
"3x6": "63.5*139.7",
"3x8": "63.5*184.15",
"3x10": "63.5*234.95",
"3x12": "63.5*285.75",
"4x4": "88.9*88.9",
"4x6": "88.9*139.7",
"4x8": "88.9*184.15",
"4x10": "88.9*234.95",
"4x12": "88.9*285.75",
"5x5": "114.3*114.3",
"6x6": "139.7*139.7",
"6x8": "139.7*190.5",
"6x10": "139.7*241.3",
"6x12": "139.7*292.1",
"8x8": "190.5*190.5",
"8x10": "190.5*241.3",
"8x12": "190.5*292.1",
"10x10": "241.3*241.3",
"10x12": "241.3*292.1",
"12x12": "292.1*292.1",}

inch_options = ["1x4", "1x6", "1x8", "1x10", "1x12", "2x4", "2x6", "2x8", "2x10", "2x12", "3x4", "3x6", "3x8", "3x10", "3x12", "4x4", "4x6", "4x8", "4x10", "4x12", "5x5", "6x6", "6x8", "6x10", "6x12", "8x8", "8x10", "8x12", "10x10", "10x12", "12x12"]

input_nominal_size = input("Please enter nominal size: ")
while input_nominal_size not in inch_options:
	print("Invalid option only {} are allowed".format(str(inch_options)))
	input_nominal_size = input("Please enter nominal size: ")

print("nominal values: {}".format(big_table[input_nominal_size]))


species_and_nominal_table = {"dou1": [47.88,8.6184,29.925,71.82,81396,29685.6],
"dou2": [43.092,8.6184,29.925,64.638,76608,27770.4],
"hem1": [46.683,7.182,19.3914,64.638,71820,26334],
"hem2": [40.698,7.182,19.3914,62.244,62244,22503.6],
"spr1": [41.895,6.4638,20.349,55.062,67032,24418.8],
"spr2": [41.895,6.4638,20.349,55.062,67032,24418.8],
}

species_nominal_mapper = {
	"1": "dou",
	"2": "hem",
	"3": "spr"
}

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


adjustments_factor = {
	2: [1.5,1.5,1.15],
	3: [1.5,1.5,1.15],
	4: [1.5,1.5,1.15],
	5: [1.4,1.4,1.1],
	6: [1.3,1.3,1.1],
	8: [1.2,1.3,1.05],
	10: [1.1,1.2,1],
	12: [1,1.1,1],
}

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




































plyform_appx_weight = {
11.9: 0.07,
12.7: 0.07,
15.1: 0.08,
15.9: 0.09,
18.25: 0.10,
19.05: 0.11,
22.22: 0.12,
25.4: 0.14,
28.6: 0.16,
}

plyform_across_class_1 = {11.9:[8372.8,1218.9,932.6],
12.7:[9768.3,1338.8,1013.3],
15.1:[14589,1673.5,1069.3],
15.9:[16491.9,1788.4,1124.2],
18.25:[22835,2148,1378.2],
19.05:[25245.4,2272.9,1413.2],
22.22:[37550.9,2917.3,1682.2],
25.4:[54169.7,3681.6,1843.3],
28.6:[70281.1,4241.1,2050.9],
}

plyform_across_class_2 = {11.9:[7992.3,1213.9,884.7],
12.7:[9514.6,1333.8,961.7],
15.1:[14589,1668.5,1047.3],
15.9:[16491.9,1783.4,1099.8],
18.25:[22835,2148,1278.9],
19.05:[25118.5,2267.9,1303.9],
22.22:[38058.3,2952.3,1571.1],
25.4:[53408.5,3766.6,1693.8],
28.6:[71803.4,4341,1882],}


plyform_across_structural_1 = {11.9:[8499.7,1228.9,885.4],
12.7:[9895.2,1353.8,965.1],
15.1:[14715.9,1688.5,986.7],
15.9:[16618.8,1803.3,1033.9],
18.25:[23215.6,2193,1201.2],
19.05:[25626,2317.9,1217],
22.22:[40215,3127.1,1482.4],
25.4:[60766.5,4131.2,1568.8],
28.6:[79034.5,4770.6,1738.5],
}


plyform_along_class_1 = {11.9:[2283.5,534.5,475.7],
12.7:[3044.7,649.4,538.6],
15.1:[3679,729.3,557.3],
15.9:[4820.7,874.2,608.4],
18.25:[9134,1233.9,746.8],
19.05:[11671.2,1528.6,798.9],
22.22:[19156,2108.1,1185.3],
25.4:[34252.5,3167.1,1379.2],
28.6:[50490.7,3991.3,1655.5],
}

plyform_along_class_2 = {11.9:[1902.9,689.4,478.6],
12.7:[2537.2,834.2,536.2],
15.1:[3171.5,939.1,552.9],
15.9:[4059.6,1124,604.5],
18.25:[7611.7,1583.6,743.5],
19.05:[9514.6,1958.2,796.2],
22.22:[15603.9,2707.5,1179.2],
25.4:[27909.5,4056.3,1373.9],
28.6:[40976.2,5110.3,1649.4],
}

plyform_along_structural_1 = {11.9:[2664.1,734.3,472.9],
12.7:[3679,889.2,535.8],
15.1:[4313.3,994.1,552.7],
15.9:[5708.8,1188.9,604.3],
18.25:[10783.2,1688.5,743.3],
19.05:[13701,2088.1,795.8],
22.22:[22708.1,2892.4,1178],
25.4:[40722.4,4346,1372.7],
28.6:[60132.2,5485,1647.2],}


plywood_weight_different = {6.78:0.038,
7.32:0.053,
10.8:0.072,
13.97:0.086,
14.43:0.105,
14.88:0.124,
20.75:0.144,
21.23:0.158,}

plywood_weight_maring = {8.69:0.038,
9.47:0.053,
13.84:0.072,
18.21:0.086,
19:0.105,
19.76:0.124,
27.71:0.144,
28.47:0.158,}


plywood_across_different = {6.78:[195.8,1014.9,294.7,395.2],
7.32:[257,3425.3,624.4,607.2],
10.8:[382.8,9768.3,1178.9,878.2],
13.97:[486.7,16365.1,1693.5,1145.2],
14.43:[567.1,24991.6,2058.1,1329.6],
14.88:[578.5,35267.4,2572.6,1582.9],
20.75:[731.7,53662.3,3317,1746.5],
21.23:[757.8,69519.9,4096.3,1943.3],}

plywood_across_marin = {8.69:[251.7,1522.3,414.6,395],
9.47:[330.3,4820.7,884.2,606.8],
13.84:[382.8,9895.2,1353.8,876.4],
18.21:[611.9,16618.8,1803.3,1166.8],
19:[756.7,25626,2317.9,1217],
19.76:[777.1,36536,2842.4,1482.4],
27.71:[1025.5,60766.5,4131.2,1568.8],
28.47:[1099.8,79034.5,4770.6,1738.5],}



plywood_along_different = {6.78:[68.4,126.9,45,397],
7.32:[123.1,253.7,114.9,690.2],
10.8:[243.8,1141.8,434.6,541.1],
13.97:[300.5,3425.3,819.3,613.3],
14.43:[409.2,7992.3,1423.7,802.1],
14.88:[521.3,13193.6,1968.2,998.5],
20.75:[622,23469.3,2952.3,1382.5],
21.23:[625.3,34379.4,3716.6,1657.2],}

plywood_along_marin = {8.69:[123.1,126.9,64.9,535.4],
9.47:[221.4,253.7,164.8,968.8],
13.84:[438.9,1776.1,614.4,535.8],
18.21:[540.9,5708.8,1188.9,604.3],
19:[736.4,13701,2088.1,795.8],
19.76:[938.3,22708.1,2892.4,992.2],
27.71:[1119.4,40722.4,4346,1372.7],
28.47:[1125.5,60132.2,5485,1647.2],}






