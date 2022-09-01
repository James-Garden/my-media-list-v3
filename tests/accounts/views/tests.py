from django.test import TestCase


class TestTests(TestCase):
    def test_tests_run(self):
        print("TEst!")
        self.assertEqual("test", 'test')
