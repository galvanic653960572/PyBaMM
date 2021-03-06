#
# Root of the pybamm module.
# Provides access to all shared functionality (simulation, models, etc.).
#
# The code in this file is adapted from Pints
# (see https://github.com/pints-team/pints)
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import sys
import os

#
# Version info: Remember to keep this in sync with setup.py!
#
VERSION_INT = 0, 0, 0
VERSION = ".".join([str(x) for x in VERSION_INT])
if sys.version_info[0] < 3:
    del (x)  # Before Python3, list comprehension iterators leaked

#
# Expose pints version
#
def version(formatted=False):
    if formatted:
        return "PyBaMM " + VERSION
    else:
        return VERSION_INT


#
# Constants
#
# Float format: a float can be converted to a 17 digit decimal and back without
# loss of information
FLOAT_FORMAT = "{: .17e}"
# Absolute path to the PyBaMM repo
script_path = os.path.abspath(__file__)
ABSOLUTE_PATH = os.path.join(os.path.split(script_path)[0], "..")

#
# Utility classes and methods
#
from .util import Timer
from .util import profile

#
# Mesh classes
#
from .mesh import Mesh

#
# Parameters class and methods
#
from .parameters.parameters import read_parameters_csv
from .parameters.parameters import Parameters
from .parameters import functions_lead_acid

#
# Simulation class
#
from .simulation import Simulation

#
# Solver class and lists of known methods
#
from .solver import Solver
from .solver import KNOWN_INTEGRATORS
from .solver import KNOWN_SPATIAL_DISCRETISATIONS

#
# Operators class
#
from .operators import Operators

#
# Variables class
#
from .variables import Variables

#
# Model classes
#
from .models.core import BaseModel
from .models.reaction_diffusion import ReactionDiffusionModel
from .models.electrolyte_current import ElectrolyteCurrentModel

#
# Submodel classes
#
from .models.submodels import electrolyte, interface

#
# Remove any imported modules, so we don't expose them as part of pybamm
#
del (sys)
