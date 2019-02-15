# -*- coding: utf-8 -*-

'''
 This file is part of pycotools3.

 pycotools3 is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 pycotools3 is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with pycotools3.  If not, see <http://www.gnu.org/licenses/>.


Author: 
    Ciaran Welsh
Date:
    12/03/2017

 Object:
 
'''


'''

    class _Config(_ConfigBase):

        def __init__(self, datasets, **kwargs):
            self.kwargs = kwargs
            self.datasets = self._DataSets(**datasets)
            self.items = self._Items(**self.kwargs.get('items', {}))
            self.settings = self._Settings(**self.kwargs.get('settings', {}))


        def __str__(self):
            return self.pretty_print({
                'settings': self.settings.kwargs,
                'datasets': self.datasets.kwargs,
                'items': self.items.kwargs,
                }
            )


        class _DataSets(_ConfigBase):
            """
            enforce the requirement for at least one experimental dataset
            but validation data sets are optional
            """

            def __init__(self, **kwargs):
                self.kwargs = kwargs
                # self.set_kwargs()
                try:
                    experiments = self.kwargs['experiments']
                except KeyError as e:
                    raise errors.InputError(
                        'The "experiments" keyword argument must be supplied.'
                    ) from e

                validations = self.kwargs.get('validations', {})

                self.experiments = self._ExperimentSet(**experiments)
                self.validations = self._ValidationSet(**validations)



            # @property
            # def defaults(self):
            #     return {
            #         'validations': self._ValidationSet(**{}).kwargs
            #     }
            #
            def __str__(self):
                return self.pretty_print(
                    {
                        'experiments': self.experiments.kwargs,
                        'validations': self.validations.kwargs,
                    }
                )

            def __repr__(self):
                return self.__str__()

            class _ExperimentSet(_ConfigBase):
                """

                If a valid argument is present, accept it. Otherwise
                add the default to the dict.

                """

                def __init__(self, **kwargs):
                    self.kwargs = kwargs
                    self.set_kwargs()
                    self.set_default_experiment_mappings()


                @property
                def defaults(self):
                    defaults = {
                        'filename': '',
                        'normalize_weights_per_experiment': True,
                        'weight_method': 'mean_squared',
                        'separator': '\t',
                        'mappings': {}
                    }
                    return defaults

            class _ValidationSet(_ConfigBase):
                def __init__(self, **kwargs):
                    self.kwargs = kwargs
                    self.set_kwargs()
                    self.set_default_experiment_mappings()

                @property
                def defaults(self):
                    return {
                        'filename': '',
                        'normalize_weights_per_experiment': True,
                        'weight_method': 'mean_squared',
                        'separator': '\t',
                        'weight': 1,
                        'threshold': 5,
                        'mappings': {},
                    }

        class _Items(_ConfigBase):
            def __init__(self, **kwargs):
                self.kwargs = kwargs

                fit_items = self.kwargs.get('fit_items', {})
                constraint_items = self.kwargs.get('constraint_items', {})

                self.fit_items = self._FitItems(**fit_items)
                self.constraint_items = self._ConstraintItems(**constraint_items)

            def __str__(self):
                return self.pretty_print({
                    'fit_items': self.fit_items.kwargs.__str__(),
                    'constraint_items': self.constraint_items.kwargs.__str__(),
                })

            def __repr__(self):
                return self.__str__()


            class _FitItems(_ConfigBase):
                def __init__(self, **kwargs):
                    self.kwargs = kwargs
                    self.set_kwargs()

                @property
                def defaults(self):
                    return {
                        'lower_bound': 1e-6,
                        'upper_bound': 1e6,
                        'start_value': 'model_value',
                        'affected_experiments': 'all',
                        'affected_validation_experiments': 'all',
                    }



            class _ConstraintItems(_ConfigBase):
                def __init__(self, **kwargs):
                    self.kwargs = kwargs
                    self.set_kwargs()

                @property
                def defaults(self):
                    return {
                        'lower_bound': 1e-6,
                        'upper_bound': 1e6,
                        'start_value': 'model_value',
                        'affected_experiments': 'all',
                        'affected_validation_experiments': 'all',
                    }

        class _Settings(_ConfigBase):
            def __init__(self, **kwargs):
                self.kwargs = kwargs
                self.set_kwargs()

            @property
            def defaults(self):
                return {
                    'copy_number': 1,
                    'pe_number': 1,
                    'results_directory': '', #os.path.join(self.model.root, 'ParameterEstimationResults'),
                    'config_filename': '', #os.path.join(self.model.root, 'config_file.yaml'),
                    'overwrite_config_file': False,
                    'update_model': False,
                    'randomize_start_values': True,
                    'create_parameter_sets': False,
                    'calculate_statistics': False,
                    'use_config_start_values': False,
                    'method': 'genetic_algorithm',
                    'number_of_generations': 200,
                    'population_size': 50,
                    'random_number_generator': 1,
                    'seed': 0,
                    'pf': 0.475,
                    'iteration_limit': 50,
                    'tolerance': 0.00001,
                    'rho': 0.2,
                    'scale': 10,
                    'swarm_size': 50,
                    'std_deviation': 0.000001,
                    'number_of_iterations': 100000,
                    'start_temperature': 1,
                    'cooling_factor': 0.85,
                    'lower_bound': 0.000001,
                    'upper_bound': 1000000,
                    'start_value': 0.1,
                    'save': False,
                    'run_mode': True,
                }
'''











import pycotools3
import unittest
import os
import pandas
import re
from Tests import _test_base
from pycotools3.tasks import ParameterEstimation
from pycotools3.utils import DotDict


def parse_timecourse(self):
    """
    read time course data into pandas dataframe. Remove
    copasi generated square brackets around the variables
    :return: pandas.DataFrame
    """

    df = pandas.read_csv(self.cls_instance.report_name, sep='\t')
    headers = [re.findall('(Time)|\[(.*)\]', i)[0] for i in list(df.columns)]
    time = headers[0][0]
    headers = [i[1] for i in headers]
    headers[0] = time
    df.columns = headers
    return df



class DotDictTests(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        from pycotools3.utils import DotDict
        dct = {'d': 4}
        dct = DotDict(dct)
        self.assertEqual(dct.d, 4)

    def test2(self):
        from pycotools3.utils import DotDict
        dct = {
            'd': {
                'c': 94
            }
        }
        dct = DotDict(dct, recursive=True)
        self.assertEqual(dct.d.c, 94)

    def test3(self):
        from pycotools3.utils import DotDict
        dct = {
            'd': {
                'c': {
                    'b': 7
                }
            }
        }
        dct = DotDict(dct, recursive=True)
        self.assertEqual(dct.d.c.b, 7)


class ParameterEstimationTestsConfig2(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationTestsConfig2, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report2.txt')

        self.TC3 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report3.txt')

        self.TC4 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report4.txt')

        self.TC5 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report5.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)
        data2 = pycotools3.misc.add_noise(self.TC2.report_name)
        data3 = pycotools3.misc.add_noise(self.TC3.report_name)
        data4 = pycotools3.misc.add_noise(self.TC4.report_name)
        data5 = pycotools3.misc.add_noise(self.TC5.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)
        os.remove(self.TC2.report_name)
        os.remove(self.TC3.report_name)
        os.remove(self.TC4.report_name)
        os.remove(self.TC5.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')
        data2.to_csv(self.TC2.report_name, sep='\t')
        data3.to_csv(self.TC3.report_name, sep='\t')
        data4.to_csv(self.TC4.report_name, sep='\t')
        data5.to_csv(self.TC5.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC3.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC4.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC5.report_name)
        self.config = ParameterEstimation.Config(
            models={
                'model1': {
                    'copasi_file': self.model.copasi_file,
                    'results_directory': os.path.join(self.model.root, 'ParameterEstimationResults')
                },
            },
            datasets={
                'experiments': {
                    'report1': {
                        'filename': self.TC1.report_name,
                        'affected_models': 'all',
                        'mappings': {
                            'Time': {
                                'model_object': 'Time',
                                'role': 'time'
                            },
                            'A': {
                                'model_object': 'A',
                                'role': 'dependent',
                            },
                        }
                    },
                    'report2': {
                        'filename': self.TC2.report_name,
                        'separator': '\t'
                    }
                },
                'validations': {
                    'report3': {
                        'filename': self.TC3.report_name,
                        'affected_models': 'model1',

                    }
                }
            },

            items={
                'fit_items': {

                    'A': {
                        'lower_bound': 15,
                        'upper_bound': 35,
                        'affected_experiments': 'report1',
                        'affected_validation_experiments': 'report3',
                        'affected_models': 'all',
                        'start_value': 17.5
                    },
                    'B': {},
                    'C': {}
                },
                'constraint_items': {
                    'C': {
                        'upper_bound': 26,
                        'lower_bound': 16
                    }
                },
            },

            settings={
                'method': 'genetic_algorithm_sr',
                'population_size': 38,
                'number_of_generations': 100,
                'copy_number': 1,
                'pe_number': 1,
                'weight_method': 'value_scaling',
                'validation_weight': 4,
                'validation_threshold': 8.5,
                'working_directory': os.path.dirname(__file__)
            }

        )
        self.PE = ParameterEstimation(self.config)

    # def test___str__(self):
    #     string = "{'model1': Model(name=New_Model, time_unit=s, volume_unit=ml, quantity_unit=mmol)}"
    #     self.assertEqual(str(self.config.models), string)

    def test_update_defaults_and_run_code(self):
        """
        1) update defaults dct
        2) build conf
        3) test that it changes appropriately
        :return:
        """
        self.PE.config.models.model1

    def test_experiment_kw1(self):
        self.assertEqual(self.PE.config.datasets.experiments.report1.filename, self.TC1.report_name)

    def test_experiment_kw2(self):
        self.assertEqual(self.PE.config.datasets.experiments.report1.separator, '\t')

    def test_experiment_kw3(self):
        self.assertEqual(self.PE.config.datasets.experiments.report2.separator, '\t')

    def test_experiment_kw4(self):
        self.assertEqual(self.PE.config.settings.weight_method, 'value_scaling')

    def test_validation_kw1(self):
        self.assertEqual(self.PE.config.datasets.validations.report3.filename, self.TC3.report_name)

    def test_validation_kw2(self):
        self.assertEqual(self.PE.config.settings.validation_weight, 4)

    def test_validation_threshold(self):
        self.assertEqual(self.config.settings.validation_threshold, self.PE.config.settings.validation_threshold)

    def test_validation_weight(self):
        self.assertEqual(self.config.settings.validation_weight, self.PE.config.settings.validation_weight)

    def test_validation_mapppings1(self):
        # self.PE.config
        self.assertEqual(self.PE.config.datasets.validations.report3.mappings.C.object_type, 'Metabolite')

    def test_mappings1(self):
        self.assertEqual(self.PE.config.datasets.experiments.report1.mappings.A.model_object, 'A')

    def test_mappings2(self):
        print(self.PE.config.model_objects)
        # self.assertEqual(self.PE.config.datasets.experiments.report1.mappings.B.model_object, 'B')

    def test_mappings3(self):
        self.assertEqual(
            self.PE.config.datasets.experiments.report2.
                mappings.B.model_object, 'B')

    def test_weight_method_updates(self):
        pass

    def test_fit_items1(self):
        self.assertEqual(self.PE.config.items.fit_items.A.lower_bound, 15)

    def test_fit_items2(self):
        self.assertEqual(self.PE.config.items.fit_items.A.affected_experiments, 'report1')

    def test_fit_items3(self):
        self.assertEqual(self.PE.config.items.fit_items.B.lower_bound, 1e-6)

    def test_constraint_items1(self):
        self.assertEqual(self.PE.config.items.constraint_items.C.lower_bound, 16)

    def test_settings1(self):
        self.assertEqual(self.PE.config.settings.method, 'genetic_algorithm_sr')

    def test_settings2(self):
        self.assertEqual(self.PE.config.settings.population_size, 38)

    def test_iteration(self):
        """
        tests that it is possible to iterate over a Conffig obj
        :return:
        """
        ## will error if cannot iter
        l = []
        for i in self.PE.config:
            l.append(i)
        expected = [
            'models',
            'datasets',
            'items',
            'settings',
        ]
        self.assertListEqual(sorted(expected), sorted(l))

    def test_affected_experiments_keyword_all_resolves1(self):
        """
        Ensure that the keyword 'all' is resolved for affected_experiments
        :return:
        """
        self.assertEqual(self.config.items.fit_items.A.affected_experiments, 'report1')

    def test_affected_experiments_keyword_all_resolves3(self):
        """
        Ensure that the keyword 'all' is resolved for affected_experiments
        :return:
        """
        self.assertListEqual(self.config.items.fit_items.C.affected_validation_experiments,
                             ['report3']
                             )

    def test_affected_experiments_keyword_all_resolves4(self):
        """
        Ensure that the keyword 'all' is resolved for affected_experiments
        :return:
        """
        self.assertListEqual(self.config.items.fit_items.C.affected_models,
                             ['model1']
                             )


class ParameterEstimationTests(_test_base._BaseTest):
    def setUp(self):
        super(ParameterEstimationTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report1.txt')

        self.TC2 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report2.txt')

        self.TC3 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report3.txt')

        self.TC4 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report4.txt')

        self.TC5 = pycotools3.tasks.TimeCourse(self.model, end=1000, step_size=100,
                                               intervals=10, report_name='report5.txt')

        ## add some noise
        data1 = pycotools3.misc.add_noise(self.TC1.report_name)
        data2 = pycotools3.misc.add_noise(self.TC2.report_name)
        data3 = pycotools3.misc.add_noise(self.TC3.report_name)
        data4 = pycotools3.misc.add_noise(self.TC4.report_name)
        data5 = pycotools3.misc.add_noise(self.TC5.report_name)

        ## remove the data
        os.remove(self.TC1.report_name)
        os.remove(self.TC2.report_name)
        os.remove(self.TC3.report_name)
        os.remove(self.TC4.report_name)
        os.remove(self.TC5.report_name)

        ## rewrite the data with noise
        data1.to_csv(self.TC1.report_name, sep='\t')
        data2.to_csv(self.TC2.report_name, sep='\t')
        data3.to_csv(self.TC3.report_name, sep='\t')
        data4.to_csv(self.TC4.report_name, sep='\t')
        data5.to_csv(self.TC5.report_name, sep='\t')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC3.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC4.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC5.report_name)


        self.conf_dct = dict(
            models=dict(
                model1=dict(
                    copasi_file=self.model.copasi_file
                    )
            ),
            datasets=dict(
                experiments=dict(
                    weight_method='value_scaling',
                    report1=dict(
                        filename=self.TC1.report_name,
                    ),
                    report4=dict(
                        filename=self.TC4.report_name
                    ),
                    report5=dict(
                        filename=self.TC5.report_name
                    )
                ),
                validations=dict(
                    weight=2.5,
                    threshold=9,
                    report2=dict(
                        filename=self.TC2.report_name
                    ),
                    report3=dict(
                        filename=self.TC3.report_name
                    )
                )
            ),
            items=dict(
                fit_items=dict(
                    A=dict(
                        affected_experiments=['report1', 'report4']
                    ),
                    B=dict(
                        affected_validation_experiments=['report2']
                    ),
                    C={},
                    A2B={},
                    B2C={},
                    B2C_0_k2={},
                    C2A_k1={},
                    ADeg_k1={},
                )
            ),
            settings=dict(
                method='genetic_algorithm_sr',
                population_size=10,
                number_of_generations=10,
                working_directory=os.path.dirname(__file__)
            )
        )
        self.conf = ParameterEstimation.Config(**self.conf_dct)

        self.PE = pycotools3.tasks.ParameterEstimation(self.conf)

        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'

    def test_load_model(self):
        self.assertIsInstance(self.PE.config.models.model1.model, pycotools3.model.Model)

    def test_output_directory_id(self):
        results_directory = os.path.join(os.path.dirname(__file__), 'Problem1/Fit1/model1/')
        self.assertEqual(self.PE.results_directory['model1'], results_directory)

    def test_get_model_obj_from_strings(self):
        self.assertEqual(len(self.PE.get_model_objects_from_strings()), 9)

    def test_metabolites(self):
        metabs = ['A', 'B', 'C']
        self.assertListEqual(sorted(metabs), sorted(self.PE.metabolites))

    def test_global_quantities(self):
        glo = ['A2B', 'ADeg_k1', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ThisIsAssignment']
        self.assertListEqual(sorted(glo), sorted(self.PE.global_quantities))

    def test_local_parameter(self):
        loc = []
        self.assertListEqual(sorted(loc), sorted(self.PE.local_parameters))

    def test_report_arguments(self):
        dct = {
            'metabolites': ['A', 'B', 'C'],
            'global_quantities': sorted(['C2A_k1', 'A2B', 'ADeg_k1', 'ThisIsAssignment', 'B2C', 'B2C_0_k2']),
            'local_parameters': [],
            'quantity_type': 'concentration',
            'report_name': 'PEData.txt', 'append': False, 'confirm_overwrite': False, 'report_type': 'multi_parameter_estimation'}
        report = self.PE._report_arguments
        for i in report:
            if isinstance(report[i], list):
                report[i] = sorted(report[i])

        self.assertEqual(report, dct)

    def test_define_report(self):
        models = self.PE._define_report()
        model = models['model1'].model
        for i in model.xml.xpath('//*[@name="Parameter Estimation"]'):
            if i.tag == '{http://www.copasi.org/static/schema}Task':
                for j in i:
                    if j.tag == '{http://www.copasi.org/static/schema}Report':
                        report = j.attrib['target']
        self.assertEqual(self.PE.config.settings.report_name, 'PEData.txt')

    def test_get_report_key(self):
        self.PE.setup()
        keys = self.PE._get_report_key()
        expected = {'model1': 'Report_32'}
        self.assertEqual(expected, keys)

    def test_get_experiment_keys1(self):
        self.PE.setup()
        experiment_keys = self.PE._get_experiment_keys()
        self.assertEqual(experiment_keys['model1']['report1'], 'Experiment_report1')

    def test_get_validation_keys1(self):
        experiment_keys = self.PE._get_validation_keys()
        self.assertEqual(experiment_keys['model1']['report2'], 'Experiment_report2')

    def test_get_experiment_keys2(self):
        experiment_keys = self.PE._get_experiment_keys()['model1']
        self.assertEqual(3, len(experiment_keys))

    # def test_write_config_file(self):
    #     """
    #     A test that PE writes the config file to the
    #     right place
    #     :return:
    #     """
    #     self.PE.write_config_file()
    #     self.assertTrue(os.path.isfile(self.PE.config_filename))


    def test_number_of_affected_experiments_is_correct(self):
        # self.PE.write_config_file()
        self.PE.setup()
        count = 0
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="Affected Experiments"]'):
            for j in i:
                count += 1

        ## only 1 of 3 experiment datasets has affected_experiments
        self.assertEqual(23, count)

    def test_number_of_affected_validation_experiments_is_correct(self):
        # self.PE.write_config_file()
        self.PE.setup()
        count = 0
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="Affected Cross Validation Experiments"]'):
            for j in i:
                count += 1

        ## only 1 of 3 experiment datasets has affected_experiments
        self.assertEqual(15, count)

    def test_affected_experiments_for_global_quantity_A2B(self):
        # self.PE.write_config_file()
        self.PE.setup()
        # self.PE.models.model1.model.open()
        count = 0
        experiment_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib['value'] == 'CN=Root,Model=New_Model,Vector=Values[A2B],Reference=InitialValue':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Experiments':
                        for k in j:
                            experiment_keys.append(k.attrib['value'])

        self.assertListEqual(sorted(['Experiment_report1', 'Experiment_report4', 'Experiment_report5']),
                             sorted(experiment_keys))

    def test_affected_validation_experiments_for_global_quantity_A2B(self):
        # self.PE.write_config_file()
        self.PE.setup()
        # self.PE.models.model1.model.open()
        count = 0
        valiadtion_keys = []
        for i in self.PE.models.model1.model.xml.findall('.//*[@name="ObjectCN"]'):
            if i.attrib['value'] == 'CN=Root,Model=New_Model,Vector=Values[A2B],Reference=InitialValue':
                for j in i.getparent():
                    if j.attrib['name'] == 'Affected Cross Validation Experiments':
                        for k in j:
                            valiadtion_keys.append(k.attrib['value'])

        self.assertListEqual(sorted(['Experiment_report2', 'Experiment_report3']),
                             sorted(valiadtion_keys))


    def test_insert_fit_items(self):
        '''
        Tests that there are the same number of rows in the template file
        as there are fit items inserted into copasi
        '''
        self.PE.setup()
        mod = self.PE.models.model1.model
        list_of_tasks = mod.xml.find(self.list_of_tasks)
        ## [5][1][3] indexes the parameter estimation item list
        optimization_item_list = list_of_tasks[5][1][3]
        self.assertEqual(8, len(optimization_item_list))

    def test_set_PE_method(self):
        '''
        test to see if method has been properly inserted into the copasi file
        '''
        self.PE.setup()
        mod = self.PE.models.model1.model
        tasks = mod.xml.find('{http://www.copasi.org/static/schema}ListOfTasks')
        for i in tasks:
            if i.attrib['name'] == 'Parameter Estimation':
                self.assertEqual(i[-1].attrib['type'].lower(), self.PE.config.settings.method.lower().replace('_', ''))

    # def test_run(self):
    #     self.PE.write_config_file()
    #     self.model = self.PE.setup()
    #     self.PE.run()
    #     f = os.path.join(self.PE.results_directory, self.PE.report_name) + '_0.txt'
    #     self.assertTrue(os.path.isfile(f))
    #
    # # def test_viz_param_est_parser(self):
    # #     """
    # #     test that viz.Parser correctly formats the
    # #     parameter estimation data
    # #     :return:
    # #     """
    # #     self.PE.write_config_file()
    # #     self.PE.setup()
    # #     self.PE.run()
    # #     p = pycotools3.viz.Parse(self.PE)
    # #     order = ['A', 'B', 'C', 'A2B', 'ADeg_k1', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ThisIsAssignment', 'RSS']
    # #     df = p.from_parameter_estimation(self.PE)
    # #     self.assertListEqual(sorted(order), sorted(list(df.columns)))
    #
    # def test_viz_param_est_parser_len(self):
    #     """
    #     outputs only one row for parameter estimation
    #     results
    #     :return:
    #     """
    #     self.PE.write_config_file()
    #     self.model = self.PE.setup()
    #     self.PE.run()
    #     import time
    #     time.sleep(2)
    #     p = pycotools3.viz.Parse(self.PE)
    #     df = p.from_multi_parameter_estimation(self.PE)
    #     self.assertEqual(df.shape[0], 1)
    #
    # #
    # def test_c(self):
    #     if os.path.isfile(self.PE.config_filename):
    #         os.remove(self.PE.config_filename)
    #     self.PE.write_config_file()
    #     self.models_dct = self.PE.setup()
    #     keys = list(self.models_dct.keys())
    #     # self.models_dct[keys[0]].open()
    #
    # def test_that_error_on_line3539_is_raised(self):
    #     pass


class ExperimentMapperTests(_test_base._BaseTest):
    def setUp(self):
        super(ExperimentMapperTests, self).setUp()

        self.TC1 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report1.txt')
        self.TC2 = pycotools3.tasks.TimeCourse(self.model,
                                               end=1000,
                                               step_size=100,
                                               intervals=10,
                                               report_name='report2.txt')

        pycotools3.misc.correct_copasi_timecourse_headers(self.TC1.report_name)
        pycotools3.misc.correct_copasi_timecourse_headers(self.TC2.report_name)

        df = pandas.read_csv(self.TC2.report_name, sep='\t')
        ## remove square brackets around species
        df = df.rename(columns={list(df.keys())[2]: list(df.keys())[2] + str('_indep')})
        self.report3 = os.path.join(os.path.dirname(self.TC2.report_name), 'report3.txt')
        df.to_csv(self.report3, sep='\t', index=False)
        assert os.path.isfile(self.report3)

        ## create some SS data for fitting
        ss_df = df.drop('Time', axis=1)
        ss_df = pandas.DataFrame(ss_df.iloc[0].transpose(), index=list(ss_df.keys())).transpose()
        self.report4 = os.path.join(os.path.dirname(self.TC2.report_name), 'report4.txt')

        ss_df.to_csv(self.report4, sep='\t', index=False)

        self.conf_dct = dict(
            models=dict(
                model1=dict(
                    copasi_file=self.model.copasi_file,
                    results_directory=os.path.join(self.model.root, 'ParameterEstimationResults'))
            ),
            datasets=dict(
                experiments=dict(
                    report1=dict(
                        filename=self.TC1.report_name,
                    ),
                    report2=dict(
                        filename=self.TC2.report_name
                    ),
                    ss=dict(
                        filename=self.report4
                    )
                ),
                validations=dict(
                    weight=2.5,
                    threshold=9,
                    report3=dict(
                        filename=self.report3
                    ),
                )
            ),
            items=dict(
                fit_items=dict(
                    A=dict(
                        affected_experiments=['report1', 'ss']
                    ),
                    B=dict(
                        affected_validation_experiments=['report3']
                    ),
                    C={},
                    A2B={},
                    B2C={},
                    B2C_0_k2={},
                    C2A_k1={},
                    ADeg_k1={},
                )
            ),
            settings=dict(
                method='genetic_algorithm_sr',
                population_size=10,
                number_of_generations=10,
                working_directory=os.path.dirname(__file__),
                weight_method = 'value_scaling',

        )
        )
        self.conf = ParameterEstimation.Config(**self.conf_dct)
        self.PE = pycotools3.tasks.ParameterEstimation(self.conf)
        # self.PE.write_config_file()
        # self.PE.setup()
        self.list_of_tasks = '{http://www.copasi.org/static/schema}ListOfTasks'


    def test_metabolite_entries(self):
        """
        test that A and B are estimated but not C
        :return:
        """
        bool = False
        for i in self.model.fit_item_order:
            if 'C' == i:
                bool = True
        self.assertFalse(bool)

    def test_global_quantity_entries(self):
        """
        :return:
        """
        bool = False
        for i in self.model.fit_item_order:
            if 'ADeg_k1' == i:
                bool = True
        self.assertFalse(bool)

    def test(self):
        self.PE._map_experiments()

    def test_correct_number_of_experiments(self):
        """
        Test that four  _experiments have been set up
        :return:
        """
        self.PE.setup()
        mod = self.PE.models['model1'].model
        count = 0
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                count += 1
        self.assertEqual(count, 3)

    def test_correct_number_of_validation_experiments(self):
        """
        Test that four  _experiments have been set up
        :return:
        """
        self.PE.setup()
        mod = self.PE.models['model1'].model
        count = 0
        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report3':
                    count += 1

        self.assertEqual(count, 1)

    def test_validation_weight(self):
        """
        Test that 2 _experiments have been set up
        :return:
        """
        self.PE.setup()
        mod = self.PE.models['model1'].model

        ans = None

        query = '//*[@name="Validation Set"]'

        for j in mod.xml.xpath(query):
            for k in list(j):
                if k.attrib['name'] == 'Weight':
                    ans = k.attrib['value']
        self.assertEqual(ans, str(self.PE.config.settings.validation_weight))

    def test_validation_threshold(self):
        """
        Test that 2 _experiments have been set up
        :return:
        """
        self.PE.setup()
        mod = self.PE.models['model1'].model

        ans = None
        query = '//*[@name="Validation Set"]'

        for j in mod.xml.xpath(query):
            for k in list(j):
                if k.attrib['name'] == 'Threshold':
                    ans = k.attrib['value']
        self.assertEqual(ans, str(self.PE.config.settings.validation_threshold))

    def test_validation(self):
        """
        Test that 2 validation _experiments have been set up
        :return:
        """
        self.PE.setup()
        mod = self.PE.models['model1'].model

        count = 0
        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] not in ['Weight', 'Threshold']:
                    count += 1
        self.assertEqual(1, count)

    def experiment_checker_function(self, expected_value, attribute):
        self.PE.setup()
        mod = self.PE.config.models.model1.model
        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report1':
                    for k in j:
                        print(k, k.attrib)
                        if k.attrib['name'] == attribute:
                            ans = k.attrib['value']
        self.assertEqual(expected_value, ans)

    def test_experiment_first_row(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('1', 'First Row')

    def test_experiment_weighting_method(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('3', 'Weight Method')

    def test_experiment_file_name(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('report1.txt', 'File Name')

    def test_experiment_number_of_columns(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.experiment_checker_function('10', 'Number of Columns')

    def test_experiment_correct_reference1(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.PE.setup()
        mod = self.PE.config.models.model1.model

        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report2':
                    for k in j:
                        if k.attrib['name'] == 'Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    ans = l[0].attrib['value']
        self.assertEqual(
            'CN=Root,Model=New_Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration',
            ans
        )

    def test_experiment_correct_reference2(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.PE.setup()
        mod = self.PE.config.models.model1.model
        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report1':
                    for k in j:
                        if k.attrib['name'] == 'Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    ans = l[0].attrib['value']
        self.assertEqual(
            'CN=Root,Model=New_Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration',
            ans,
        )

    def test_validation_map1(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.PE.setup()
        mod = self.PE.config.models.model1.model

        ans = None
        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report3':
                    for k in j:
                        if k.attrib['name'] == 'Object Map':
                            for l in k:
                                if l.attrib['name'] == '1':
                                    ans = l[0].attrib['value']
        self.assertEqual(
            ans,
            'CN=Root,Model=New_Model,Vector=Compartments[nuc],Vector=Metabolites[A],Reference=Concentration'
        )

    def test_experiment_steady_state(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.PE.setup()
        mod = self.PE.config.models.model1.model
        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'ss':
                    for k in j:
                        if k.attrib['name'] == 'Experiment Type':
                            ## code for steady state is '0'
                            ans = k.attrib['value']
        self.assertEqual(str(0), ans)

    def test_experiment_time_course(self):
        """
        First row of experiment_0==1
        :return:
        """

        self.PE.setup()
        mod = self.PE.config.models.model1.model

        ans = None
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                if j.attrib['name'] == 'report1':
                    for k in j:
                        if k.attrib['name'] == 'Experiment Type':
                            ## code for steady state is '0'
                            ans = k.attrib['value']
        self.assertEqual(ans, str(1))

    def test_experiment_correct_number_of_object_maps(self):
        """
        First row of experiment_0==1
        :return:
        """

        self.PE.setup()
        mod = self.PE.config.models.model1.model

        count = 0
        query = '//*[@name="Experiment Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(3, count)

    def test_experiment_correct_number_of_validation_obj_maps(self):
        """
        First row of experiment_0==1
        :return:
        """
        self.PE.setup()
        mod = self.PE.config.models.model1.model

        count = 0

        query = '//*[@name="Validation Set"]'
        for i in mod.xml.xpath(query):
            for j in i:
                for k in j:
                    if k.attrib['name'] == 'Object Map':
                        count += 1
        self.assertEqual(1, count)

    def test_get_experiment_keys(self):
        dct = self.PE._get_experiment_keys()
        self.assertEqual(dct['model1']['report1'], 'Experiment_report1')

    def test_get_validation_keys(self):
        dct = self.PE._get_validation_keys()
        print(dct)
        self.assertEqual(dct['model1']['report3'], 'Experiment_report3')

    def test_create_experiments(self):
        from lxml import etree
        elements = self.PE._map_experiments(validation=False)
        self.assertIsInstance(elements['model1']['report1'], etree._Element)

    def test_create_validation_experiments(self):
        from lxml import etree
        elements = self.PE._map_experiments(validation=True)
        self.assertIsInstance(elements['model1']['report3'], etree._Element)

    def test_fit_items_property(self):
        lst = ['A', 'B', 'C', 'A2B', 'B2C', 'B2C_0_k2', 'C2A_k1', 'ADeg_k1']
        self.assertListEqual(sorted(lst), sorted(list(self.PE.config.items.fit_items.keys())))

    def test_remove_fit_item(self):
        self.PE

    def test_correct_number_of_fit_items(self):
        self.PE.setup()
        query = '//*[@name="FitItem"]'
        count = 0
        for i in self.PE.models.model1.model.xml.xpath(query):
            if i.attrib['name'] == 'FitItem':
                count += 1
        self.assertEqual(count, 8)


    def test_set_PE_method(self):
        self.PE.setup()
        mod = self.PE.models.model1.model

        query = '//*[@name="Parameter Estimation"]'
        ans = None
        for i in mod.xml.xpath(query):
            if i.tag == '{http://www.copasi.org/static/schema}Task':
                for j in i:
                    print(j.tag)
                    if j.tag == 'Method':
                        ans = j.attrib['name']
        self.assertEqual('Genetic Algorithm SR', ans)





if __name__ == '__main__':
    unittest.main()
























