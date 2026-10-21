import io
import unittest
from contextlib import redirect_stdout

from service_name.__main__ import main


class ServiceTests(unittest.TestCase):
    def test_main(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            main()
        self.assertEqual(output.getvalue(), "Hello from <SERVICE-NAME>!\n")
