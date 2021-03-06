#
# Shared methods and classes for testing
#
import pybamm


class VarsForTesting(object):
    def __init__(self, t=None, c=None, e=None, j=None):
        self.t = t
        self.c = c
        self.e = e
        self.j = j


def pdes_io(model):
    y = model.initial_conditions()
    vars = pybamm.Variables(model)
    vars.update(0, y)
    dydt = model.pdes_rhs(vars)
    return y, dydt
