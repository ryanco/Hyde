import unittest
import CommandLineTests
import HydeArgTests
import JekyllPostTests
import JekyllDraftPostTests
import JekyllPageTests
import ConfigTests
import PublishPostTest

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(CommandLineTests)
suite.addTests(loader.loadTestsFromModule(HydeArgTests))
suite.addTests(loader.loadTestsFromModule(JekyllPostTests))
suite.addTests(loader.loadTestsFromModule(JekyllDraftPostTests))
suite.addTests(loader.loadTestsFromModule(JekyllPageTests))
suite.addTests(loader.loadTestsFromModule(ConfigTests))
suite.addTests(loader.loadTestsFromModule(PublishPostTest))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
