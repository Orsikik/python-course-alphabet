import unittest
import calc

class CalcTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        print('setUpClass')
        print('==========')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass')
        print('==========')

    def setUp(self):
        print(f'Set up for {self.shortDescription()}')

    def TearDown(self):
        print(f'Set up for {self.shortDescription()}')

    def test_add(self):
        """Test_add"""
        self.assertEqual(calc.add(1, 2), 3)

    def test_sub(self):
        """"Test_sub"""
        self.assertEqual(calc.sub(5, 2), 3)

    def test_mul(self):
        """Test_mul"""
        self.assertEqual(calc.mul(5, 2), 10)

    def test_div(self):
        """Test_div"""
        self.assertEqual(calc.div(8, 4), 2)


if __name__ == '__main__':
    unittest.main()