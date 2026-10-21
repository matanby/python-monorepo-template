import unittest

import package_name


class PackageTests(unittest.TestCase):
    def test_package_is_importable(self) -> None:
        self.assertEqual(package_name.__name__, "package_name")
