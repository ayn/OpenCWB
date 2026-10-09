"""Exercise bundled resources without importing Home Assistant."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'custom_components/opencwb/core'


class CityResourcesTest(unittest.TestCase):
    def test_bundled_city_files(self):
        prefix = '_city_resource_test'
        names = [prefix, prefix + '.commons', prefix + '.weatherapi12',
                 prefix + '.weatherapi12.location', prefix + '.commons.cityidregistry']
        try:
            for name, path in [(prefix, ROOT), (prefix + '.commons', ROOT / 'commons'),
                               (prefix + '.weatherapi12', ROOT / 'weatherapi12')]:
                spec = importlib.util.spec_from_file_location(
                    name, path / '__init__.py', submodule_search_locations=[str(path)])
                sys.modules[name] = importlib.util.module_from_spec(spec)
            location = types.ModuleType(prefix + '.weatherapi12.location')
            location.Location = object
            sys.modules[location.__name__] = location
            spec = importlib.util.spec_from_file_location(
                names[-1], ROOT / 'commons/cityidregistry.py')
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            registry = module.CityIDRegistry.get_instance()
            for letter in ('a', 'g', 'm', 's'):
                lines = list(registry._get_lines(registry._assess_subfile_from(letter)))
                self.assertTrue(lines)
                self.assertTrue(all(isinstance(line, str) for line in lines))
                self.assertIn(',', lines[0])
        finally:
            for name in reversed(names):
                sys.modules.pop(name, None)


if __name__ == '__main__':
    unittest.main()
