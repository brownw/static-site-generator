import unittest

from extract_title import *


class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        md = "# This is a title"
        title = "This is a title"
        self.assertEqual(extract_title(md), title)

if __name__ == "__main__":
    unittest.main()