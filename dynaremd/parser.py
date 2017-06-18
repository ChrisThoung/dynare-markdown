# -*- coding: utf-8 -*-
"""
parser
======
Module to parse Markdown files and their Dynare code.

"""

import itertools
import re


class Equation(object):

    pattern = re.compile(
        r'''(?: [{] (?P<parameter> [A-Za-z][_A-Za-z0-9]* ) [}] ) |
            (?:     (?P<variable>  [A-Za-z][_A-Za-z0-9]* )     )
        ''', re.VERBOSE)

    function_list = ['exp']

    def __init__(self, script):
        self.script = script
        self.endogenous, self.exogenous, self.parameters, self.functions = self.parse(self.script, self.pattern, self.function_list)

    @staticmethod
    def parse(script, pattern, function_list):
        """Return the endogenous, exogenous and parameter variables in `script`, along with any variables that appear in `function_list`.

        Logic
        -----
        1. Split the equation script at '=', into LHS and RHS scripts.
        2. Break each side into variables and parameters (LHS variables are
           endogenous, RHS variables are exogenous)
        3. Reclassify terms as functions if they appear in `function_list`
        4. Resolve duplicates in order of precedence: parameters, endogenous,
           exogenous

        """

        def separate(iterable):
            """Group the match elements in iterable by type, storing to a dict
            of lists.

            Example
            -------
            `iterable` is an iterable of `re.Match` objects with groupdicts as
            follows:
                [
                    {'parameter': 'beta', 'variable': None},
                    {'parameter': None, 'variable': 'c'},
                    {'parameter': None, 'variable': 'r'},
                    {'parameter': 'delta', 'variable': None},
                ]

            This becomes:
                {
                    'parameter': ['beta', 'delta'],
                     'variable': ['c', 'r'],
                }

            """
            groups = {}

            for match in iterable:
                # Drop all keys where the value is `None`
                term = {k: v for k, v in match.groupdict().items()
                             if v is not None}
                assert len(term) == 1
                k, v = term.popitem()

                groups[k] = groups.get(k, []) + [v]

            return groups

        # 1. Split into LHS and RHS parts -------------------------------------
        split = script.split('=')
        assert len(split) == 2

        # 2. Separate and classify by type ------------------------------------
        lhs, rhs = map(separate, map(pattern.finditer, split))

        # LHS variables are endogenous
        endogenous = set(lhs.get('variable', []))
        # RHS variables are exogenous
        exogenous = set(rhs.get('variable', []))
        # Parameters can be on either side
        parameters = set(lhs.get('parameter', []) + rhs.get('parameter', []))

        # 3. Functions are any terms also listed in `function_list` -----------
        functions = set(
            term
            for term in itertools.chain(endogenous, exogenous, parameters)
            if term in function_list
        )

        # 4. Resolve duplicates -----------------------------------------------
        parameters = parameters.difference(functions)
        endogenous = endogenous.difference(parameters).difference(functions)
        exogenous = exogenous.difference(endogenous).difference(parameters).difference(functions)

        return list(map(sorted, [endogenous, exogenous, parameters, functions]))


class Model(object):

    # Default equation-parser class
    parser = Equation

    def __init__(self, equations):
        self.scripts = equations
        self.endogenous, self.exogenous, self.parameters, self.functions = self.parse(self.scripts, self.parser)

    @staticmethod
    def parse(scripts, parser):
        #  Parse individual equations
        equations = list(map(parser, scripts))

        # Extract variables by type
        endogenous = set(itertools.chain.from_iterable(e.endogenous for e in equations))
        exogenous = set(itertools.chain.from_iterable(e.exogenous for e in equations))
        parameters = set(itertools.chain.from_iterable(e.parameters for e in equations))
        functions = set(itertools.chain.from_iterable(e.functions for e in equations))

        # Resolve duplicates by imposing precedence: functions, parameters,
        # endogenous, exogenous
        parameters = parameters.difference(functions)
        endogenous = endogenous.difference(parameters).difference(functions)
        exogenous = exogenous.difference(endogenous).difference(parameters).difference(functions)

        return list(map(sorted, [endogenous, exogenous, parameters, functions]))
