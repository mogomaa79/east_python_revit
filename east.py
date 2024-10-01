from Systems import *

# Example usage:
if __name__ == "__main__":
    system_choice = get_int("Systems are: \nTraditional System (1)\nProps System (2)\nFast System (3)\nEast System (4)\nFrames System (5)\nPlease Choose (1-5): ", 1, 5)
    if system_choice == 1: system = TraditionalSystem()
    elif system_choice == 2: system = PropsSystem()
    elif system_choice == 3: system = FastSystem()
    elif system_choice == 4: system = EastSystem()
    elif system_choice == 5: system = FramesSystem()

    system.run()
