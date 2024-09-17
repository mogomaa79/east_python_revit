from bisect import bisect_right
from utils import *

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

class Sheathing:
    def __init__(self, concrete_weight_plus_live_load=0):
        self.is_plywood = None
        self.ply_class = None
        self.is_face_grain_across = None
        self.sheathing_values = None
        self.final_parameter = None
        self.final_sheathing_weight = None
        self.concrete_weight_plus_live_load = concrete_weight_plus_live_load

    def _get_sheathing_info(self):
        """Get sheathing details from user."""
        plywood_or_plyform = input("Please choose between Plywood (1) and Plyform (2): ")
        while plywood_or_plyform not in ["1", "2"]:
            plywood_or_plyform = input("Invalid option! Please choose between Plywood (1) and Plyform (2): ")
        self.is_plywood = plywood_or_plyform == "1"

        if not self.is_plywood:
            self.ply_class = input("Please choose between Class I (1), Class II (2), Structural I (3): ")
            while self.ply_class not in ["1", "2", "3"]:
                self.ply_class = input("Invalid Option! Please choose between Class I, Class II, or Structural I (1, 2, 3): ")
        else:
            self.ply_class = input("Please choose between Structural I and Marine (1), another class for different species (2): ")
            while self.ply_class not in ["1", "2"]:
                self.ply_class = input("Invalid Option! Please choose between Structural I and Marine (1), another class (2): ")

        self.is_face_grain_across = input("Please choose between face grain across (1) or along (2): ")
        while self.is_face_grain_across not in ["1", "2"]:
            self.is_face_grain_across = input("Invalid Option! Please choose face grain across (1) or along (2): ")
        return self.is_plywood, self.ply_class, self.is_face_grain_across

    def _get_sheathing_thickness(self):
        """
        Function to gather the sheathing thickness and related parameters based on user input.
        Different options are provided for plyform, plywood, and species classes.
        Returns the final values and parameters used in further calculations.
        """
        # For Plyform sheathing
        if not self.is_plywood:
            input_plyform_thickness = float(input("Please enter plyform thickness: "))
            while input_plyform_thickness not in plyform_thickness:
                print(f"Invalid option. Only {', '.join(map(str, plyform_thickness))} are allowed.")
                input_plyform_thickness = float(input("Please enter plyform thickness: "))

            final_sheathing_thickness = input_plyform_thickness
            final_sheathing_weight = plyform_weight_by_thickness[final_sheathing_thickness]
            final_parameter = plyform_general_mapper[f"{self.ply_class}_{self.is_face_grain_across}"][final_sheathing_thickness]

        # For Plywood with different species
        elif self.ply_class == "2":
            input_species_thickness = float(input("Please enter different species thickness: "))
            while input_species_thickness not in different_species_thickness:
                print(f"Invalid option. Only {', '.join(map(str, different_species_thickness))} are allowed.")
                input_species_thickness = float(input("Please enter different species thickness: "))

            final_sheathing_thickness = input_species_thickness
            final_sheathing_weight = plywood_weight_different[final_sheathing_thickness]
            final_parameter = plywood_across_different[final_sheathing_thickness] if self.is_face_grain_across == "1" else plywood_along_different[final_sheathing_thickness]

        # For Plywood with Structural/Marine type
        elif self.ply_class == "1":
            input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
            while input_structural_marine_thickness not in structural_marine_thickness:
                print(f"Invalid option. Only {', '.join(map(str, structural_marine_thickness))} are allowed.")
                input_structural_marine_thickness = float(input("Please enter structural marine thickness: "))
            final_sheathing_thickness = input_structural_marine_thickness
            final_sheathing_weight = plywood_weight_marine[final_sheathing_thickness]
            final_parameter = plywood_across_marine[final_sheathing_thickness] if self.is_face_grain_across == "1" else plywood_along_marine[final_sheathing_thickness]

        # Output the results of the thickness calculations
        print(f"Final Sheathing Thickness: {final_sheathing_thickness}")
        print(f"Final Sheathing Weight: {final_sheathing_weight}")
        print(f"Final Parameters: {final_parameter}\n")

        sheathing_values = {}
        
        # Additional input required if plywood is selected
        if self.is_plywood:
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
                    sheathing_values[k] = v[stress_group][index]
            
            sheathing_values["Fs"] = rolling_shear_table[self.ply_class][index]

        # If Plyform is selected, assign stress values based on the class
        else:
            sheathing_values = plyform_stress[self.ply_class]

        # Output final values and return them
        print("Final Values:")
        for k, v in sheathing_values.items():
            print(f"{k}: {v}")
        self.sheathing_values = sheathing_values
        self.final_parameter = final_parameter
        self.final_sheathing_weight = final_sheathing_weight
    
    def _get_sheathing_distance(self):
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
        fb = self.sheathing_values["Fb"]
        fs = self.sheathing_values["Fs"]
        E = self.sheathing_values["E"]

        print(f"fb: {fb:.2f}")
        
        # Shear factor based on plywood or plyform selection
        se_index = 2 if self.is_plywood else 1
        sheathing_se = self.final_parameter[se_index]

        rolling_shear = self.final_parameter[-1]  # Rolling shear value
        print(f"rs: {rolling_shear}")
        print(f"se: {sheathing_se}")
        print(f"wb: {self.concrete_weight_plus_live_load}")
        
        print(f"fs: {fs:.2f}")
        print(f"E: {E}")
        
        # Moment of inertia based on plywood or plyform selection
        i_index = 1 if self.is_plywood else 0
        final_parameter_i = self.final_parameter[i_index]
        print(f"I: {final_parameter_i:.2f}")

        # Design span input
        design_span = float(input("Enter design span (m): ")) * 1000  # Convert to millimeters

        # Calculate lb (based on bending stress and concrete weight)
        lb_constant = 120 if no_of_spans == 3 else 96
        lb = (((lb_constant * fb * sheathing_se) / self.concrete_weight_plus_live_load) ** 0.5) / 1000 

        # Calculate ls (based on shear stress and rolling shear)
        ls = (ls_constant_mapper[no_of_spans] * fs * rolling_shear) / (self.concrete_weight_plus_live_load * 1000)

        # Deflection constraints
        deflection_a_input = design_span / 360
        deflection_b_input = design_span / 16
        deflection_a_equation = ((1743 * E * final_parameter_i) / (360 * self.concrete_weight_plus_live_load)) ** (1/3) / 1000
        deflection_b_equation = ((1743 * E * final_parameter_i) / (16 * self.concrete_weight_plus_live_load)) ** (1/4) / 1000
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
        return joist_dist, no_of_spans

    def get_sheathing_distance(self):
        """Get sheathing distance based on user input."""
        self._get_sheathing_info()
        self._get_sheathing_thickness()
        return self._get_sheathing_distance()
    
class Joisting:
    def __init__(self, weight_on_joists=0, no_of_spans=0, rolling_shear=0):
        self.nominal_size, self.joist_i, self.joist_s, self.joist_values = get_characteristics()
        self.weight_on_joists = weight_on_joists
        self.no_of_spans = no_of_spans
        self.rolling_shear = rolling_shear

    def calculate_stringing_distance(self):
        """Calculate joist-related values."""
        try:
            thickness, width = map(int, self.nominal_size.split("x"))
            fb_factor = adjustments_factor[width][thickness]
        except:
            fb_factor = 1

        cd = 0.9  # Duration factor
        new_fb = fb_factor * cd * self.joist_values["Fb"]
        lb_constant = 120 if self.no_of_spans == 3 else 96
        joist_lb = ((lb_constant * new_fb * self.joist_s * 1e-9) / self.weight_on_joists) ** 0.5
        
        if self.no_of_spans == 3:
            joist_ls = (20 * self.joist_values["Fv"] * self.rolling_shear * 1e-4) / self.weight_on_joists
        else:
            breadth, depth = map(float, inch_to_metric[self.nominal_size].split("*"))
            joist_ls = (16 * self.joist_values["Fv"] * breadth * depth * 1e-6) / 2 + 2 * depth * 1e-3
        
        if self.no_of_spans == 3:
            deflection_360 = ((1743 * self.joist_values["E"] * self.joist_i) / (360 * self.weight_on_joists)) ** (1/3)
            deflection_16 = ((1743 * self.joist_values["E"] * self.joist_i) / (16 * self.weight_on_joists)) ** (1/4)
        else:
            deflection_360 = ((4608 * self.joist_values["E"] * self.joist_i) / (1800 * self.weight_on_joists)) ** (1/3)
            deflection_16 = ((4608 * self.joist_values["E"] * self.joist_i) / (80 * self.weight_on_joists)) ** (1/4)

        return min(joist_lb, joist_ls, deflection_360, deflection_16)

class Shores:
    def __init__(self):
        self.shores_values = None
        self.shores_i = None
        self.shores_s = None

    def calculate_shores_values(self, shores_values, shores_i, shores_s, weight_on_joists, nominal_size):
        """Calculate shores-related values."""
        try:
            thickness, width = map(int, self.nominal_size.split("x"))
            fb_factor = adjustments_factor[width][thickness]
        except:
            fb_factor = 1

        cd = 0.9
        new_fb = fb_factor * cd * shores_values["Fb"]
        shores_lb = ((120 * new_fb * shores_s * 1e-9) / weight_on_joists) ** 0.5
        breadth, depth = map(float, inch_to_metric[nominal_size].split("*"))
        shores_ls = (192 * shores_values["Fv"] * breadth * depth * 1e-6) / (15 * weight_on_joists) + 2 * depth * 1e-3

        deflection_360 = ((1743 * shores_values["E"] * shores_i) / (360 * weight_on_joists)) ** (1/3)
        deflection_16 = ((1743 * shores_values["E"] * shores_i) / (16 * weight_on_joists)) ** (1/4)

        return shores_lb, shores_ls, deflection_360, deflection_16

class Props:
    def calculate_props_distance(self, concrete_weight_plus_live_load):
        """Calculate props distance based on load."""
        r1 = float(input("Please enter r1: "))
        r2 = float(input("Please enter r2: "))
        mass = float(input("Please enter mass of props: "))
        y = float(input("Please enter y: "))
        inertia = 0.5 * mass * (r1 ** 2 + r2 ** 2)
        e = float(input("Please enter Modulus of Elasticity: "))
        fv = float(input("Please enter fv: "))
        fb = float(input("Please enter fb: "))

        lb = (120 * fb * inertia / concrete_weight_plus_live_load) ** 0.5
        lv = (192 * fv * r1 * r2 / (15 * concrete_weight_plus_live_load)) + 2 * r1

        deflection_360 = ((1743 * e * inertia) / (360 * concrete_weight_plus_live_load)) ** (1/3)
        deflection_16 = ((1743 * e * inertia) / (16 * concrete_weight_plus_live_load)) ** (1/4)

        return min(lb, lv, deflection_360, deflection_16)

class BaseSystem:
    def __init__(self):
        self.concrete_weight = self.calculate_concrete_weight()
        self.sheathing = Sheathing(self.concrete_weight)

    def calculate_concrete_weight(self):
        """Calculate concrete weight plus live load."""
        unit_weight_of_concrete = float(input("Please enter unit weight of concrete: "))
        thickness_of_slab = float(input("Please enter thickness of slab: "))
        suitable_live_load = float(input("Please enter suitable live load: "))
        is_motorized = input("Please choose Motorized (1) or Non-motorized (2): ")

        while is_motorized not in ["1", "2"]:
            is_motorized = input("Invalid Option! Please choose Motorized (1) or Non-motorized (2): ")

        final_option = motorized_options if is_motorized == "1" else non_motorized_options

        concrete_weight = round(unit_weight_of_concrete * thickness_of_slab, 2)
        print(f"Concrete Weight: {concrete_weight}")

        concrete_weight_plus_live_load = concrete_weight + suitable_live_load
        print(f"Concrete Weight plus Live Load: {concrete_weight_plus_live_load}")

        final_thickness = thickness_options[bisect_right(thickness_options, thickness_of_slab)]
        print(f"Final Thickness: {final_thickness}")

        concrete_weight_plus_live_load = max(final_option[final_thickness], concrete_weight_plus_live_load)
        print(f"Final Concrete Weight plus Live Load: {concrete_weight_plus_live_load}\n")

        return concrete_weight_plus_live_load
    
    def run(self):
        joist_dist, _ = self.sheathing.get_sheathing_distance()
        print(f"Final distance between joists: {joist_dist}")
        

class TraditionalSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self.joisting = None
        self.shores = Shores()

    def run(self):
        joist_dist, n_spans = self.sheathing.get_sheathing_distance()
        print(f"Final distance between joists: {joist_dist}")

        total_load = self.sheathing.concrete_weight_plus_live_load + self.sheathing.final_sheathing_weight
        self.joisting = Joisting(total_load, n_spans, self.sheathing.final_parameter[-1])
        stringing_dist = self.joisting.calculate_stringing_distance()
        print(f"Final distance between joists: {stringing_dist}")

    def run_traditional_calculations(self, concrete_weight_plus_live_load):
        """Run calculations for the traditional system, including joisting and shores."""
        sheathing_values, final_parameter, final_sheathing_weight = self.run_sheathing_calculations()

        self.nominal_size, joist_i, joist_s, joist_values = self.joisting.get_characteristics()
        joist_lb, joist_ls = self.joisting.calculate_joist_values(joist_s, joist_values, 0, concrete_weight_plus_live_load, 2, self.nominal_size)

        shores_lb, shores_ls, deflection_360, deflection_16 = self.shores.calculate_shores_values({}, 0, 0, concrete_weight_plus_live_load, self.nominal_size)
        print(f"Final shores distance: {shores_lb}, {shores_ls}")

class PropsSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self.props = Props()

    def run_props_calculations(self, concrete_weight_plus_live_load):
        """Run calculations for the props system."""
        sheathing_values, final_parameter, final_sheathing_weight = self.run_sheathing_calculations()
        props_distance = self.props.calculate_props_distance(concrete_weight_plus_live_load)
        print(f"Final props distance: {props_distance}")

# Example usage:
if __name__ == "__main__":
    system_choice = input("Select system: Traditional (1) or Props (2): ")
    if system_choice == "1":
        system = TraditionalSystem()
    else:
        system = PropsSystem()

    if system_choice == "1":
        system.run()
    else:
        system.run()
