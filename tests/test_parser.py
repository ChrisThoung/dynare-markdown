# -*- coding: utf-8 -*-
"""
test_parser
===========
Test equations come from the model in Chapter 3 of Tommaso Mancini Griffoli's
Dynare User Guide:
http://www.dynare.org/documentation-and-support/user-guide

"""


from dynaremd.parser import Equation, Model


def test_equation():
    script = '(1/c) = beta*(1/c(+1))*(1+r(+1)-delta);'

    euler = Equation(script)

    assert euler.endogenous == ['c']
    assert euler.exogenous == ['beta', 'delta', 'r']
    assert euler.parameters == []
    assert euler.functions == []

def test_equation_with_parameters():
    script = '{psi}*c/(1-l) = w;'

    labour_supply = Equation(script)

    assert labour_supply.endogenous == ['c', 'l']
    assert labour_supply.exogenous == ['w']
    assert labour_supply.parameters == ['psi']
    assert labour_supply.functions == []


def test_model():
    equations = [
        '(1/c) = beta*(1/c(+1))*(1+r(+1)-delta);',
        'psi*c/(1-l) = w;',
        'c+i = y;',
        'y = (k(-1)^alpha)*(exp(z)*l)^(1-alpha);',
        'w = y*((epsilon-1)/epsilon)*(1-alpha)/l;',
        'r = y*((epsilon-1)/epsilon)*alpha/k(-1);',
        'i = k-(1-delta)*k(-1);',
        'y_l = y/l;',
        'z = rho*z(-1)+e;',
    ]

    model = Model(equations)

    assert model.endogenous == ['c', 'i', 'l', 'psi', 'r', 'w', 'y', 'y_l', 'z']
    assert model.exogenous == ['alpha', 'beta', 'delta', 'e', 'epsilon', 'k', 'rho']
    assert model.parameters == []
    assert model.functions == ['exp']

def test_model_with_parameters():
    equations = [
        '(1/c) = {beta}*(1/c(+1))*(1+r(+1)-{delta});',
        '{psi}*c/(1-l) = w;',
        'c+i = y;',
        'y = (k(-1)^{alpha})*(exp(z)*l)^(1-{alpha});',
        'w = y*(({epsilon}-1)/{epsilon})*(1-{alpha})/l;',
        'r = y*(({epsilon}-1)/{epsilon})*{alpha}/k(-1);',
        'i = k-(1-{delta})*k(-1);',
        'y_l = y/l;',
        'z = {rho}*z(-1)+e;',
    ]

    model = Model(equations)

    assert model.endogenous == ['c', 'i', 'l', 'r', 'w', 'y', 'y_l', 'z']
    assert model.exogenous == ['e', 'k']
    assert model.parameters == ['alpha', 'beta', 'delta', 'epsilon', 'psi', 'rho']
    assert model.functions == ['exp']
