from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "dynamic_display",
    version = "1.5",
    description = "Dynamic display of a fitness center scores. Should be running on a raspberry PI or like, displayed on a screen",
    executables = [Executable("dynamic-display/main.py")],
)
