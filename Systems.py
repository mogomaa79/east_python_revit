from Processes import *
from bisect import bisect_right


class BaseSystem:
    def __init__(self):
        self.concrete_weight = self.calculate_concrete_weight()
        self.sheathing = Sheathing(self.concrete_weight)

    def calculate_concrete_weight(self):
        """Calculate concrete weight plus live load."""
        unit_weight_of_concrete = get_float("Please enter unit weight of concrete: ")
        thickness_of_slab = get_float("Please enter thickness of slab: ")
        suitable_live_load = get_float("Please enter suitable live load: ")
        is_motorized = get_int(
            "Please choose Motorized (1) or non-motorized (2): ", 1, 2
        )

        final_option = (
            motorized_options if is_motorized == "1" else non_motorized_options
        )

        concrete_weight = round(unit_weight_of_concrete * thickness_of_slab, 2)
        print(f"Concrete Weight: {concrete_weight}")

        concrete_weight_plus_live_load = concrete_weight + suitable_live_load
        print(f"Concrete Weight plus Live Load: {concrete_weight_plus_live_load}")

        final_thickness = thickness_options[
            bisect_right(thickness_options, thickness_of_slab)
        ]
        print(f"Final Thickness: {final_thickness}")

        concrete_weight_plus_live_load = max(
            final_option[final_thickness], concrete_weight_plus_live_load
        )
        print(
            f"Final Concrete Weight plus Live Load: {concrete_weight_plus_live_load}\n"
        )

        return concrete_weight_plus_live_load

    def run(self):
        joist_dist, _ = self.sheathing.get_sheathing_distance()
        print(f"Final distance between joists: {joist_dist}")


class TraditionalSystem(BaseSystem):
    def __init__(self):
        super().__init__()
        self.joisting = None
        self.shores = None
        self.total_load = 0

    def _run_stringer(self):
        joist_dist, n_spans = self.sheathing.get_sheathing_distance()
        print(f"Final distance between joists: {joist_dist}\n")

        self.total_load = (
            self.sheathing.concrete_weight_plus_live_load
            + self.sheathing.final_sheathing_weight
        )
        self.joisting = Joisting(
            self.total_load, n_spans, self.sheathing.final_parameter[-1]
        )
        stringing_dist = self.joisting.get_stringing_distance()
        print(f"Final distance between stringers: {stringing_dist}\n")
        return joist_dist, stringing_dist

    def run(self):
        joist_dist, stringing_dist = self._run_stringer()
        self.shores = Shores(self.total_load)
        shores_dist = self.shores.get_shores_distance()

        print(f"\nFinal distance between joists: {joist_dist}")
        print(f"Final distance between stringers: {stringing_dist}")
        print(f"Final distance between shores: {shores_dist}")


class PropsSystem(TraditionalSystem):
    def __init__(self):
        super().__init__()
        self.props = None

    def run(self):
        joist_dist, stringing_dist = self._run_stringer()
        self.props = Props(self.total_load)
        props_dist = self.props.calculate_props_distance()

        print(f"\nFinal distance between joists: {joist_dist}")
        print(f"Final distance between stringers: {stringing_dist}")
        print(f"Final distance between props: {props_dist}")


class FastSystem(BaseSystem):
    pass


class EastSystem(BaseSystem):
    pass


class FramesSystem(TraditionalSystem):
    def __init__(self):
        super().__init__()
        self.frames = None

    def run(self):
        joist_dist, stringing_dist = self._run_stringer()
        self.frames = Frames(self.total_load)
        crit_x, crit_y = self.frames.calculate_critical_load()

        print(f"\nFinal distance between joists: {joist_dist}")
        print(f"Final distance between stringers: {stringing_dist}")
        if crit_x > self.total_load:
            print(f"Section in X direction is SAFE")
        else:
            print(f"Section in X direction is NOT SAFE")
            return

        if crit_y > self.total_load:
            print(f"Section in Y direction is SAFE")
        else:
            print(f"Section in Y direction is NOT SAFE")
            return

        dist_x, dist_y = self.frames.calculate_frames_dist()
        print(f"Distance in X-Direction: {dist_x}")
        print(f"Distance in Y-Direction: {dist_y}")
