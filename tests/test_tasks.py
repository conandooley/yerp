__author__ = 'Conan Dooley'

import os.path
import unittest
from deployment.fabfile.task import YmlParser, Task


class TaskTest(unittest.TestCase):
    def test_parsing(self):
        config_file = os.path.dirname(os.path.realpath(__file__)) + "/test_config.yml"
        parser = YmlParser()
        tasks = parser.parse(config_file)

        for task in tasks:
            self.assertIsInstance(task, Task)
            if task.name == "config_dhcpd":
                self.assertEqual("em1", task.configs[0].options["internal_if"])
                self.assertTrue('external_interface' in task.configs[0].options)
            if task.name == "only_commands":
                self.assertEquals(0, len(task.configs))
                self.assertTrue("sudo apt_get install" in task.commands)

if __name__ == '__main__':
    unittest.main()
