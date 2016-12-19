import unittest
import pkg_resources

examples = ['example{}.py'.format(i) for i in range(1, 4)]
import PyDAQmx

class Test(unittest.TestCase):
    def test(self):
        for name in examples:
            src = pkg_resources.resource_string(__name__, name)
            code = compile(src, name, 'exec')
            exec(code, globals())


