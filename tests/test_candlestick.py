import unittest
import paths_for_tests
from app.market_reader.candlestick import Candlestick

class Test_Candlestick(unittest.TestCase):
    def test_basic_methods(self):
        cs = Candlestick()
        cs.open = 100
        cs.high = 110
        cs.low= 91
        cs.close = 95 

        self.assertEqual(cs.sign(),-1)
        self.assertEqual(cs.body(), 5)
        self.assertEqual(cs.wick_upper(),10)
        self.assertEqual(cs.wick_lower(),4)
        self.assertEqual(cs.range(),19)
        wick_upper,body,wick_lower = cs.percent_parts()
        self.assertAlmostEqual(wick_upper,52.63,2)
        self.assertAlmostEqual(body,26.32,2)
        self.assertAlmostEqual(wick_lower,21.05,2)
        #self.ass









if __name__=='__main__':
    unittest.main()
