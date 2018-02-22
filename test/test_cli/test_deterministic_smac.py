import json
import os
import sys
import unittest
import shutil
from nose.plugins.attrib import attr

from unittest import mock

from smac.smac_cli import SMACCLI


class TestDeterministicSMAC(unittest.TestCase):

    def setUp(self):
        base_directory = os.path.split(__file__)[0]
        base_directory = os.path.abspath(
            os.path.join(base_directory, '..', '..'))
        self.current_dir = os.getcwd()
        os.chdir(base_directory)

        self.output_dir_1 = "test/test_files/out_test_deterministic_1"
        self.output_dir_2 = "test/test_files/out_test_deterministic_2"
        self.output_dir_3 = "test/test_files/out_test_deterministic_3"
        self.scenario_file = "test/test_files/test_deterministic_scenario.txt"
        self.output_dirs = [self.output_dir_1, self.output_dir_2, self.output_dir_3]

        self.maxDiff = None

    def tearDown(self):
        for output_dir in self.output_dirs:
            if output_dir:
                shutil.rmtree(output_dir, ignore_errors=True)
        os.chdir(self.current_dir)

    @attr('slow')
    def test_deterministic(self):
        """
        Testing deterministic behaviour.
        """
        testargs = ["scripts/smac",
                    "--scenario", self.scenario_file,
                    "--verbose_level", "DEBUG",
                    "--seed", "1",
                    "--random_configuration_chooser", "test/test_cli/random_configuration_chooser_impl.py",
                    "--output_dir", self.output_dir_1]
        SMACCLI().main_cli(testargs[1:])
        testargs = ["scripts/smac",
                    "--scenario", self.scenario_file,
                    "--verbose_level", "DEBUG",
                    "--seed", "1",
                    "--random_configuration_chooser", "test/test_cli/random_configuration_chooser_impl.py",
                    "--output_dir", self.output_dir_2]
        SMACCLI().main_cli(testargs[1:])
        testargs = ["scripts/smac",
                    "--scenario", self.scenario_file,
                    "--verbose_level", "DEBUG",
                    "--seed", "2",
                    "--random_configuration_chooser", "test/test_cli/random_configuration_chooser_impl.py",
                    "--output_dir", self.output_dir_3]
        SMACCLI().main_cli(testargs[1:])
        # compare trajectories in output_dir_{1,2,3}
        h1 = json.load(open(self.output_dir_1 + '/run_1/runhistory.json'))
        h2 = json.load(open(self.output_dir_2 + '/run_1/runhistory.json'))
        h3 = json.load(open(self.output_dir_3 + '/run_2/runhistory.json'))
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
