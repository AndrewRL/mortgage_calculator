from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from calculator import MortgageCalculator
from validation import *
from errors import *

calc = MortgageCalculator()

def unpack_params(params, query_keys):
    print(params)
    result = []
    for key in query_keys:
        result.append(params[key])

    return result

async def recurring_payment(request):

    params = dict(request.query_params)

    # Verify that the required arguments have been passed
    required_keys = ['asking_price', 'down_payment', 'payment_schedule', 'amortization_period']
    for key in required_keys:
        if key not in params.keys():
            raise HTTPException(HTTP_400_BAD_REQUEST, f'The required query parameter "{key}" is missing.')

    # Remove any extraneous parameters sent with the request
    for key in params.keys():
        if key not in required_keys:
            del(params[key])

    # Convert the user provided values to the appropriate data types
    param_dtypes = {key: calc.param_dtypes[key] for key in required_keys}
    unconverted_params = params
    params = convert_params(params, param_dtypes)
    if params is None:
        for param in unconverted_params:
            result = convert_param(param, calc.param_dtypes)
            if result is None:
                raise HTTPException(HTTP_400_BAD_REQUEST, f'The parameter {param} is malformed.')

    # Validate the values provided by the user for each query param
    validators = ValidatorHandler()
    validators.add('asking_price', AskingPriceValidationError, validate_positive_float)
    validators.add('down_payment', DownPaymentValidationError, validate_positive_float)
    validators.add('payment_schedule', PaymentScheduleValidationError, validate_payment_schedule, calc.annual_payments)
    validators.add('amortization_period',
                   AmortizationPeriodValidationError,
                   validate_positive_integer_in_range,
                   calc.minimum_amortization_period,
                   calc.maximum_amortization_period)

    errors = validators.validate_all(params, required_keys)
    if errors:
        raise errors[0]

    asking_price, down_payment, payment_schedule, amortization_period = unpack_params(params, required_keys)

    # Calculate the recurring payment
    mortgage = calc.payment_per_period(asking_price, down_payment, payment_schedule, amortization_period)

    if mortgage.status == 'declined':
        return JSONResponse({'mortgage_status': 'declined', 'reason': mortgage.status_text})
    else:
        return JSONResponse({'payment_per_period': mortgage.payment_per_period})


async def maximum_mortgage(request):
    params = dict(request.query_params)
    required_keys = ['payment', 'payment_schedule', 'amortization_period']
    for key in required_keys:
        if key not in params.keys():
            raise HTTPException(HTTP_400_BAD_REQUEST, f'The required query parameter "{key}" is missing.')

    # Remove any extraneous parameters sent with the request
    for key in params.keys():
        if key not in required_keys:
            del (params[key])


    # Convert the query strings to the appropriate data types
    param_dtypes = {key: calc.param_dtypes[key] for key in required_keys}
    unconverted_params = params
    params = convert_params(params, param_dtypes)
    if params is None:
        for param in unconverted_params:
            result = convert_param(param, param_dtypes[param])
            if result is None:
                raise HTTPException(HTTP_400_BAD_REQUEST, f'The parameter {param} is malformed.')

    # Strip and convert string to lowercase for comparison to allowed keys
    params['payment_schedule'] = clean_string(params['payment_schedule'])

    validators = ValidatorHandler()
    validators.add('payment', PaymentValidationError, validate_positive_float)
    validators.add('payment_schedule', PaymentScheduleValidationError, validate_payment_schedule, calc.annual_payments)
    validators.add('amortization_period',
                   AmortizationPeriodValidationError,
                   validate_positive_integer_in_range,
                   calc.minimum_amortization_period,
                   calc.maximum_amortization_period + 1)

    errors = validate_params(params, required_keys, validators)
    if errors:
        raise errors[0]

    payment, payment_schedule, amortization_period = unpack_params(params, required_keys)

    max_mortgage = calc.maximum(payment, payment_schedule, amortization_period)
    return JSONResponse({'maximum_mortgage': max_mortgage})


async def change_interest_rate(request):
    # Validate the user provided interest rate
    json = await request.json()
    new_rate = json['interest_rate']
    if not isinstance(new_rate, float):
        new_rate = convert_param(new_rate, float)
    if new_rate is None:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'The interest rate provided cannot be converted to a float. ' +
                                                    'Make sure it does not contain any non-numeric characters.')
    validator = Validator(InterestRateValidationError, validate_positive_float)
    error = validator.validate(new_rate)
    if error:
        raise error

    old_rate = calc.interest_rate
    calc.interest_rate = new_rate / 100

    return JSONResponse({'old_interest_rate': old_rate, 'new_interest_rate': new_rate})


app = Starlette(debug=True, routes=[
    Route('/payment-amount', recurring_payment, methods=['GET']),
    Route('/mortgage-amount', maximum_mortgage, methods=['GET']),
    Route('/interest-rate', change_interest_rate, methods=['PATCH'])
])