import unittest
from mutation_check import classify

class MutationClassifierTests(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(classify(lambda:1,lambda:2,1),'killed')
        self.assertEqual(classify(lambda:1,lambda:1,1),'survived')
        self.assertEqual(classify(lambda:2,lambda:3,1),'invalid_baseline')
        self.assertEqual(classify(lambda:1,lambda:1/0,1),'error')
        self.assertEqual(classify(lambda:1/0,lambda:2,1),'error')

if __name__ == '__main__': unittest.main()
