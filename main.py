import mcschematic
from assembler import assemble
from simulator import simulate
from schematic import make_schematic
import argparse
import os

parser = argparse.ArgumentParser(prog="Assembler")
parser.add_argument("filename")
args = parser.parse_args()

if "SCHEMATIC_PATH" not in os.environ:
    print("SCHEMATIC_PATH environment variable must be set")
    exit(1)

path = os.environ["SCHEMATIC_DIR"]

name = "program"
version = mcschematic.Version.JE_1_18_2


def assemble_to_schematic(assembly_filename):
    global path, name, version
    machine_code_layer = "output.mc"
    assemble(assembly_filename, machine_code_layer)
    make_schematic(machine_code_layer, path, name, version)


def assemble_and_simulate(assembly_filename):
    machine_code_layer = "output.mc"
    assemble(assembly_filename, machine_code_layer)
    simulate(machine_code_layer)


def main():
    program = args.filename
    assemble_to_schematic(program)
    # assemble_and_simulate(f'programs/{program}.as')


if __name__ == "__main__":
    main()
