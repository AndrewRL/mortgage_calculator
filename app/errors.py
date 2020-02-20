from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

class ValidationError(HTTPException):
    def __init__(self, error_text='The parameter could not be validated.'):
        super().__init__(HTTP_400_BAD_REQUEST, f'Parameter validation failed: {error_text}')

class AskingPriceValidationError(ValidationError):
    def __init__(self):
        super().__init__('The asking price must be a positive whole number or decimal >= 0.')

class DownPaymentValidationError(ValidationError):
    def __init__(self):
        super().__init__('The down payment must be a positive whole number or decimal >= 0 and cannot exceed the asking price.')

class PaymentScheduleValidationError(ValidationError):
    def __init__(self):
        super().__init__('The allowed values for "payment_schedule" are "weekly", "biweekly", and "monthly".')

class AmortizationPeriodValidationError(ValidationError):
    def __init__(self):
        super().__init__('The amortization period must be a whole number between 5 and 25 (inclusive).')

class PaymentValidationError(ValidationError):
    def __init__(self):
        super().__init__('The payment must be a positive whole number or decimal >= 0.')

class InterestRateValidationError(ValidationError):
    def __init__(self):
        super().__init__('The interest rate must be expressed as a percentage >= 0., such as 3.99 or 15. Decimal values are treated as percentages less than 1%')


class ConversionError(HTTPException):
    pass