from errors import *

class Validator:
    def __init__(self, error, func, *args):
        self.error = error
        self.func = func
        self.args = args

    def validate(self, value):
        result = self.func(value, *self.args)
        error = None
        if not result:
            error = self.error
        return error

class ValidatorHandler:
    def __init__(self, validators=None):
        self.validators = validators if validators is not None else {}

    def add(self, key, error, func, *args):
        self.validators[key] = Validator(error, func, *args)

    def validate_all(self, params, query_keys):
        validators = self.validators
        errors = None
        for key in query_keys:
            param = params[key]
            validator = validators[key]
            error = validator.validate(param)
            if error:
                if errors is None:
                    errors = []
                errors.append(error)
        return errors

def validate_params(params, query_keys, validators):
    validators = validators.validators
    errors = []
    for key in query_keys:
        param = params[key]
        validator = validators[key]
        error = validator.validate(param)
        if error:
            errors.append(error)
    return errors

def validate_positive_float(value):
    if not validate_float(value):
        return False
    return validate_positive_value(value)

def validate_float(value):
    return isinstance(value, float)

def validate_integer(value):
    return isinstance(value, int)

def validate_positive_value(value):
    return value >= 0

def validate_value_in_range(value, low, high):
    return low <= value < high

def validate_positive_integer_in_range(value, low, high):
    # Check if the value is truly an integer first to prevent errors in other validators
    if not validate_integer(value):
        return False
    return all((validate_positive_value(value), validate_value_in_range(value, low, high)))

def validate_payment_schedule(payment_schedule, payment_schedules):
    if payment_schedule not in payment_schedules.keys():
        return False
    return True

def convert_params(params, dtypes):
    if params.keys() != dtypes.keys():
        raise ValueError('The keys to the params dict and the dtypes dict must by the same.')

    if not params:
        return {}

    for key in params.keys():
        value = params[key]
        result = convert_param(value, dtypes[key])
        if result is not None:
            params[key] = result
        else:
            return None

    return params

def convert_param(param, dtype):
    try:
        param = dtype(param)
    except ValueError:
        return None

    return param

def clean_string(value):
    return value.strip().lower()
