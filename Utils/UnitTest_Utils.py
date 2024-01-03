# coding: utf-8
import unittest


class TestStringMethods(unittest.TestCase):
    # preparation init test
    def setUp(self):
        # 每一个测试前都会执行
        print('test begin!')

    def tearDown(self):
        # 每一个测试后都会执行
        print('end test!')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        print('aa')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
