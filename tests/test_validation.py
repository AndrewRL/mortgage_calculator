import unittest
from app.validation import *

class TestValidatePositiveFloat(unittest.TestCase):
    def test_positive_value(self):
        value = 1.
        result = validate_positive_float(value)
        self.assertEqual(result, True)

    def test_negative_value(self):
        value = -1.
        result = validate_positive_float(value)
        self.assertEqual(result, False)

    def test_zero_value(self):
        value = 0.
        result = validate_positive_float(value)
        self.assertEqual(result, True)

    def test_integer_value(self):
        value = 1
        result = validate_positive_float(value)
        self.assertEqual(result, False)

    def test_string_value(self):
        value = 'text'
        result = validate_positive_float(value)
        self.assertEqual(result, False)


class TestValidateFloat(unittest.TestCase):
    def test_float_value(self):
        value = 1.
        result = validate_float(value)
        self.assertEqual(result, True)

    def test_integer_value(self):
        value = 1
        result = validate_float(value)
        self.assertEqual(result, False)

    def test_string_value(self):
        value = '1.'
        result = validate_float(value)
        self.assertEqual(result, False)


class TestValidateInteger(unittest.TestCase):
    def test_float_value(self):
        value = 1.
        result = validate_integer(value)
        self.assertEqual(result, False)

    def test_integer_value(self):
        value = 1
        result = validate_integer(value)
        self.assertEqual(result, True)

    def test_string_value(self):
        value = '1'
        result = validate_integer(value)
        self.assertEqual(result, False)


class TestValidatePositiveValue(unittest.TestCase):
    def test_positive_integer(self):
        value = 1
        result = validate_positive_value(value)
        self.assertEqual(result, True)

    def test_negative_integer(self):
        value = -1
        result = validate_positive_value(value)
        self.assertEqual(result, False)

    def test_positive_float(self):
        value = 1.
        result = validate_positive_value(value)
        self.assertEqual(result, True)

    def test_negative_float(self):
        value = -1.
        result = validate_positive_value(value)
        self.assertEqual(result, False)

    def test_non_numeric_value(self):
        value = 'text'
        self.assertRaises(TypeError, validate_positive_value, value)

    def test_zero_values(self):
        self.assertEqual(validate_positive_value(0), True)
        self.assertEqual(validate_positive_value(0.), True)


class TestValidateValueInRange(unittest.TestCase):
    def test_min_value(self):
        low = 5
        high = 10
        value = 5
        self.assertEqual(validate_value_in_range(value, low, high), True)

    def test_max_value(self):
        low = 5
        high = 10
        value = 10
        self.assertEqual(validate_value_in_range(value, low, high), False)

    def test_float_values(self):
        self.assertEqual(validate_value_in_range(5., 5., 10.), True)
        self.assertEqual(validate_value_in_range(10., 5., 10.), False)

    def test_non_numeric_value(self):
        self.assertRaises(TypeError, validate_value_in_range, 'text', 5, 10)


class TestValidatePositiveIntegerInRange(unittest.TestCase):
    def test_min_value(self):
        self.assertEqual(validate_positive_integer_in_range(1, 1, 10), True)

    def test_max_value(self):
        self.assertEqual(validate_positive_integer_in_range(10, 1, 10), False)

    def test_non_integer(self):
        self.assertEqual(validate_positive_integer_in_range(1., 1, 10), False)
        self.assertEqual(validate_positive_integer_in_range('text', 1, 10), False)

    def test_negative_value(self):
        self.assertEqual(validate_positive_integer_in_range(-1, -1, 0), False)


class TestValidatePaymentSchedule(unittest.TestCase):
    def test_existing_key(self):
        payment_schedule = 'weekly'
        payment_schedules = {'weekly': 52, 'biweekly': 26, 'monthly': 12}
        self.assertEqual(validate_payment_schedule(payment_schedule, payment_schedules), True)

    def test_non_existant_key(self):
        payment_schedule = 'daily'
        payment_schedules = {'weekly': 52, 'biweekly': 26, 'monthly': 12}
        self.assertEqual(validate_payment_schedule(payment_schedule, payment_schedules), False)

    def test_non_string(self):
        payment_schedule = 1
        payment_schedules = {'weekly': 52, 'biweekly': 26, 'monthly': 12}
        self.assertEqual(validate_payment_schedule(payment_schedule, payment_schedules), False)


class TestConvertParam(unittest.TestCase):
    def test_allowed_conversion(self):
        result = convert_param('1.', float)
        self.assertEqual(result, 1.)
        self.assertIsInstance(result, float)

        result = convert_param('1', float)
        self.assertEqual(result, 1.)
        self.assertIsInstance(result, float)

    def test_disallowed_conversions(self):
        result = convert_param('1..', int)
        self.assertIsNone(result)

        result = convert_param('1%', float)
        self.assertIsNone(result)


class TestConvertParams(unittest.TestCase):
    def test_empty_params_dict(self):
        params = {}
        dtypes = {}
        result = convert_params(params, dtypes)
        self.assertEqual(result, {})

    def test_params_dtypes_mismatch(self):
        params = {'param1': '1'}
        dtypes = {'param1': float, 'param2': float}
        self.assertRaises(ValueError, convert_params, params, dtypes)

    def test_successful_conversion(self):
        params = {'param1': '1', 'param2': '1.'}
        dtypes = {'param1': int, 'param2': float}
        result = convert_params(params, dtypes)
        self.assertEqual(result, {'param1': 1, 'param2': 1.})

class MockParams:
    def __init__(self):
        self.params = {'param1': 10, 'param2': 10., 'param3': 'text'}
        self.query_keys = ['param1', 'param2']
        self.validators = ValidatorHandler()
        self.validators.add('param1', ValidationError, validate_positive_integer_in_range, 5, 25)
        self.validators.add('param2', ValidationError, validate_float)


class TestValidateParams(unittest.TestCase):

    def test_mismatched_keys(self):
        v = MockParams()
        v.query_keys = ['param1', 'param2', 'param3']
        self.assertRaises(KeyError, v.validators.validate_all, v.params, v.query_keys)

    def test_successful_validation(self):
        v = MockParams()
        result = v.validators.validate_all(v.params, v.query_keys)
        self.assertEqual(result, None)

    def test_empty_args(self):
        v = MockParams()
        v.params = {}
        v.query_keys = []
        v.validators = ValidatorHandler()
        result = v.validators.validate_all(v.params, v.query_keys)
        self.assertIsNone(result)

    def test_malformed_validators(self):
        v = MockParams()
        v.validators = ValidatorHandler()
        v.validators.add('param1', ValidationError, validate_positive_integer_in_range, 'weekly')
        v.validators.add('param2', ValidationError, validate_float)
        self.assertRaises(TypeError, v.validators.validate_all, v.params, v.query_keys)


class TestValidator(unittest.TestCase):
    def test_validation(self):
        value = 20
        validator = Validator(ValidationError, validate_positive_integer_in_range, 5, 26)
        result = validator.validate(value)
        self.assertIsNone(result)

    def test_mismatched_args(self):
        value = 20.5
        validator = Validator(validate_positive_integer_in_range, 'weekly')
        self.assertRaises(TypeError, validator.validate, value)

if __name__ == '__main__':
    unittest.main()
