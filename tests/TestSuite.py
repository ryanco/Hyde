import unittest
import CommandLineTests
import HydeMainTests
import JekyllPostTests
import JekyllDraftPostTests
import JekyllPageTests

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(CommandLineTests)
suite.addTests(loader.loadTestsFromModule(HydeMainTests))
suite.addTests(loader.loadTestsFromModule(JekyllPostTests))
suite.addTests(loader.loadTestsFromModule(JekyllDraftPostTests))
suite.addTests(loader.loadTestsFromModule(JekyllPageTests))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
