import unittest
import pkg_resources
from .test_Task import _TestWithDevice

examples = ['example{}.py'.format(i) for i in range(1, 5)]
import PyDAQmx

class Test(object):
    name = None
    def test(self):
        src = pkg_resources.resource_string(__name__, self.name)
        code = compile(src, self.name, 'exec')
        exec(code, globals())

for i, name in enumerate(examples):
    the_class = type('Test{i}'.format(i=i), (Test, _TestWithDevice), {'name':name})
    exec('Test{i}=the_class'.format(i=i))
