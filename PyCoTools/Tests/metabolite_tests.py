#-*-coding: utf-8 -*-
"""

 This file is part of PyCoTools.

 PyCoTools is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 PyCoTools is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with PyCoTools.  If not, see <http://www.gnu.org/licenses/>.


 $Author: Ciaran Welsh


"""

import site
site.addsitedir('C:\Users\Ciaran\Documents\PyCoTools')
import PyCoTools
from PyCoTools.Tests import _test_base
import os, glob
import pandas
import unittest



class TestMetabolites(_test_base._BaseTest):
    def setUp(self):
        super(TestMetabolites, self).setUp()
        self.nucleus = PyCoTools.model.Compartment(name='Nuc', value=5,
                                                   type='fixed', key='compartment_1')
        self.A = PyCoTools.model.Metabolite(name='A', compartment=self.nucleus,
                                             concentration=5)
    def test_string_method(self):
        """

        :return:
        """
        string =  "Metabolite(compartment=Compartment(key='compartment_1',  name='Nuc',  type='fixed',  value=5), concentration=5, name='A')"
        self.assertEqual(string, self.A.__str__())

    def test_error(self):
        """
        test that Metabolite raises error if
        neither particle number or concentration
        is called.

        Learn how to do this when you have internet
        :return:
        """
        pass

    def test_name(self):
        self.assertEqual(self.A.name, 'A')

    def test_compartment(self):


        self.assertEqual(self.A.compartment, self.nucleus)

    def test_reference_initial(self):
        self.assertEqual(self.A.reference_initial, 'Vector=Metabolites[A],Reference=InitialConcentration')

    def test_reference_transient(self):
        self.assertEqual(self.A.reference_transient, 'Vector=Metabolites[A],Reference=Concentration')

    def test_particle_numbers(self):
        A = PyCoTools.model.Metabolite(particle_number=10e23, compartment=self.nucleus)
        self.assertTrue(A.particle_number, 10e23)

    def test_concentration(self):
        """
        Test metabolite particle number to concentration conversion

        When concentration is changed, particle numbers change accordingly
        When particle number is changes, concenrtation is changes accordingly
        :param self:
        :return:
        """
        A = PyCoTools.model.Metabolite(concentration=5, compartment=self.nucleus)
        self.assertTrue(A.concentration, 5)


class TestSubstrate(_test_base._BaseTest):
    def setUp(self):
        super(TestSubstrate, self).setUp()
        self.nucleus = PyCoTools.model.Compartment(name='Nuc', value=5,
                                                   type='fixed', key='compartment_1')
        self.A = PyCoTools.model.Substrate(name='A', compartment=self.nucleus,
                                           concentration=5, particle_number=5,
                                           stoiciometry=1, reaction_key='reaction_1')

    def test_name(self):
        self.assertEqual(self.A.name, 'A')

    def test_comp(self):
        self.assertEqual(self.A.compartment, self.nucleus)

    def test_concentration(self):
        self.assertEqual(self.A.concentration, 5)

    def test_stoiciometry(self):
        self.assertEqual(self.A.stoiciometry, 1)

    def test_reaction_key(self):
        self.assertEqual(self.A.reaction_key, 'reaction_1')

    def test_to_substrate(self):
        # print self.B.to_substrate()
        self.assertTrue(isinstance(self.A.to_substrate(), PyCoTools.model.Substrate))


class TestProduct(_test_base._BaseTest):
    def setUp(self):
        super(TestProduct, self).setUp()
        self.nucleus = PyCoTools.model.Compartment(name='Nuc', value=5,
                                                   type='fixed', key='compartment_1')
        self.B = PyCoTools.model.Product(name='B', compartment=self.nucleus,
                                         concentration=60,
                                         stoiciometry=1, reaction_key='reaction_1',
                                         particle_number=1220)

    def test_name(self):
        self.assertEqual(self.B.name, 'B')

    def test_comp(self):
        self.assertEqual(self.B.compartment, self.nucleus)

    def test_concentration(self):
        self.assertEqual(self.B.concentration, 60)

    def test_stoiciometry(self):
        self.assertEqual(self.B.stoiciometry, 1)

    def test_reaction_key(self):
        self.assertEqual(self.B.reaction_key, 'reaction_1')



if __name__=='__main__':
    unittest.main()







