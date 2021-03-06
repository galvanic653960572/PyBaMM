#
# Equation classes for the electrolyte
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

import numpy as np


class StefanMaxwellDiffusion(object):
    """Equations for the electrolyte."""

    def __init__(self, subparam, suboperators, submesh, tests):
        """
        Assign simulation-specific objects as attributes.

        Parameters
        ----------
        subparam : :class:`pybamm.parameters.Parameters` subclass instance
            The parameters of the simulation
        suboperators : :class:`pybamm.operators.Operators` subclass instance
            The spatial operators.
        submesh : :class:`pybamm.mesh.Mesh` subclass instance
            The spatial and temporal discretisation.
        tests : dict
            A dictionary for testing the convergence of the numerical solution:
                * {} (default): We are not running in test mode, use built-ins.
                * {'inits': dict of initial conditions,
                   'bcs': dict of boundary conditions,
                   'sources': dict of source terms
                   }: To be used for testing convergence to an exact solution.
        """
        # Apply attributes
        self.subparam = subparam
        self.suboperators = suboperators
        self.submesh = submesh
        self.tests = tests

    def initial_conditions(self):
        """Calculates initial conditions for variables in the electrolyte.

        Returns
        -------
        array_like
            The initial conditions
        """
        if not self.tests:
            return self.subparam.c0 * np.ones_like(self.submesh.centres)
        else:
            return self.tests["inits"]["concentration"]

    def pdes_rhs(self, vars):
        """Conservation of cations.

        Parameters
        ----------
        vars : array_like, shape (n,)
            The variables of the simulation
        flux_bcs : 2-tuple of array_like, shape (1,)
            Flux at the boundaries (Neumann BC).

        Returns
        -------
        dcdt : array_like, shape (n,)
            The time derivative of c.

        """
        if not self.tests:
            flux_bcs = self.bcs()
            j = vars.j
        else:
            flux_bcs = self.tests["bcs"](vars.t)["concentration"]
            j = self.tests["sources"](vars.t)["concentration"]

        # Calculate internal flux
        N_internal = -self.suboperators.grad(vars.c)

        # Add boundary conditions (Neumann)
        flux_bc_left, flux_bc_right = flux_bcs
        N = np.concatenate([flux_bc_left, N_internal, flux_bc_right])

        # Calculate time derivative
        dcdt = -self.suboperators.div(N) + self.subparam.s * j

        return dcdt

    def bcs(self):
        """Flux boundary conditions for the cation conservation equation.

        Returns
        -------
        2-tuple of array_like, shape(1,)
            The boundary conditions.

        """
        flux_bc_left = np.array([0])
        flux_bc_right = np.array([0])
        return (flux_bc_left, flux_bc_right)

    # def current_conservation(self, domain, c, e, j, current_bcs):
    #     """The 1D diffusion equation.
    #
    #     Parameters
    #     ----------
    #     subparam : pybamm.parameters.Parameter() instance
    #         The parameters of the simulation
    #     variables : 2-tuple (c, e) of array_like, shape (n,)
    #         The concentration, and potential difference.
    #     operators : pybamm.operators.Operators() instance
    #         The spatial operators.
    #     j : array_like, shape (n,)
    #         Interfacial current density.
    #     current_bcs : 2-tuple of array_like, shape (1,)
    #         Flux at the boundaries (Neumann BC).
    #
    #     Returns
    #     -------
    #     dedt : array_like, shape (n,)
    #         The time derivative of the potential.
    #
    #     """
    #     # Calculate current density
    #     i = self.macinnes(domain, c, e, current_bcs)
    #
    #     # Calculate time derivative
    #     if domain == "xcn":
    #         gamma_dl = self.subparam.gamma_dl_n
    #     elif domain == "xcp":
    #         gamma_dl = self.subparam.gamma_dl_p
    #
    #     dedt = 1 / gamma_dl * (self.operators[domain].div(i) - j)
    #
    #     return dedt
    #
    # def macinnes(self, domain, c, e, current_bcs):
    #     """MacInnes equation for the electrolyte current density.
    #
    #     Parameters
    #     ----------
    #     domain : string
    #         The domain in which to calculate the electrolyte current density.
    #     c : array_like, shape (n,)
    #         The electrolyte concentration.
    #     e : array_like, shape (n,)
    #         The potential difference.
    #     current_bcs : 2-tuple of array_like, shape (1,)
    #         Flux at the boundaries (Neumann BC).
    #
    #     Returns
    #     -------
    #     i : array_like, shape (n+1,)
    #         The current density.
    #     """
    #     operators = self.operators[domain]
    #     kappa_over_c = 1
    #     kappa = 1
    #
    #     # Calculate inner current
    #     i_inner = kappa_over_c * operators.grad(c) + kappa * operators.grad(e)
    #
    #     # Add boundary conditions
    #     lbc, rbc = current_bcs
    #     i = np.concatenate([lbc, i_inner, rbc])
    #
    #     return i
    #
    # def bcs_current(self, domain, t):
    #     """Boundary conditions for the current conservation equation.
    #
    #     Returns
    #     -------
    #     2-tuple of array_like, shape(1,)
    #         The boundary conditions.
    #
    #     """
    #     if domain == "xcn":
    #         current_bc_left = np.array([0])
    #         current_bc_right = np.array([self.subparam.icell(t)])
    #     elif domain == "xcp":
    #         current_bc_left = np.array([self.subparam.icell(t)])
    #         current_bc_right = np.array([0])
    #     return (current_bc_left, current_bc_right)
