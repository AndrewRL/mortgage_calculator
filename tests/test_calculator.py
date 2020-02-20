from app.calculator import *
import unittest

class TestDownPaymentPercentage(unittest.TestCase):
    def test_down_payment_percentage(self):
        asking_price = 100000.
        down_payment = 5000.
        result = down_payment_percentage(asking_price, down_payment)
        self.assertEqual(result, .05)

    def test_no_down_payment(self):
        asking_price = 100000.
        down_payment = 0.
        result = down_payment_percentage(asking_price, down_payment)
        self.assertEqual(result, 0.)

    def test_max_down_payment(self):
        asking_price = 100000.
        down_payment = 100000.
        result = down_payment_percentage(asking_price, down_payment)
        self.assertEqual(result, 1.)

class TestMinimumDownPayment(unittest.TestCase):
    def test_no_asking_price(self):
        asking_price = 0.
        result = minimum_down_payment(asking_price)
        self.assertEqual(result, 0.)

    def test_low_asking_price(self):
        asking_price = 100000.
        result = minimum_down_payment(asking_price)
        self.assertEqual(result, 5000.)

    def test_breakpoint_asking_price(self):
        asking_price = 500000.
        result = minimum_down_payment(asking_price)
        self.assertEqual(result, 25000.)

    def test_high_asking_price(self):
        asking_price = 1000000.
        result = minimum_down_payment(asking_price)
        self.assertEqual(result, 75000)

# TODO: Make these minimal test cases
class TestCalculateInsuranceCost(unittest.TestCase):
    def test_no_insurance_required(self):
        insurance_tiers = [
            {'min': .05, 'max': .0999, 'rate': .0315},
            {'min': .1, 'max': .1499, 'rate': .024},
            {'min': .15, 'max': .1999, 'rate': .018},
            {'min': .2, 'max': 1.00, 'rate': 0}
        ]
        asking_price = 100000.
        down_payment = 20000.
        result = calculate_insurance_cost(insurance_tiers, asking_price, down_payment)
        self.assertEqual(result, 0.)

    def test_insurance_required(self):
        insurance_tiers = [
            {'min': .05, 'max': .0999, 'rate': .0315},
            {'min': .1, 'max': .1499, 'rate': .024},
            {'min': .15, 'max': .1999, 'rate': .018},
            {'min': .2, 'max': 1.00, 'rate': 0}
        ]
        asking_price = 100.
        down_payment = 19.99
        result = calculate_insurance_cost(insurance_tiers, asking_price, down_payment)
        self.assertEqual(result, 1.8)

    def test_insurance_tiers(self):
        insurance_tiers = [
            {'min': .05, 'max': .0999, 'rate': .0315},
            {'min': .1, 'max': .1499, 'rate': .024},
            {'min': .15, 'max': .1999, 'rate': .018},
            {'min': .2, 'max': 1.00, 'rate': 0}
        ]
        asking_price = 100.
        down_payments = [5., 9.99, 10., 14.99, 15., 19.99, 20, 100.]
        expected = [3.15, 3.15, 2.4, 2.4, 1.8, 1.8, 0, 0]
        for index, down_payment in enumerate(down_payments):
            result = calculate_insurance_cost(insurance_tiers, asking_price, down_payment)
            self.assertEqual(result, expected[index])

    def test_no_applicable_tier(self):
        insurance_tiers = [
            {'min': .05, 'max': .1, 'rate': .05}
        ]
        asking_price = 100.
        down_payment = 1.
        self.assertRaises(ValueError, calculate_insurance_cost, insurance_tiers, asking_price, down_payment)


if __name__ == '__main__':
    unittest.main()