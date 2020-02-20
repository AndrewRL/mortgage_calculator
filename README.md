Mortgage Calculator API

This API provides the following methods which are useful for calculating mortgage information:

GET /payment-amount

    Params:
    asking_price: Whole number or decimal greater than or equal to 0.
    down_payment: Whole number of decimal greater than or equal to 0 and less than or equal to the asking price.
    payment_schedule: "weekly", "biweekly", or "monthly"
    amortization_period: Whole number between 5 and 25 inclusive.

    Returns a json object with the key "payment_per_period" and the payment amount if the mortgage is allowed.
    Returns a json object with the keys "mortgage_status" = "declined" and the reason if the mortgage is rejected.

GET /mortgage-amount

    Params:
    payment: Numeric value greater than or equal to 0.
    payment_schedule: "weekly", "biweekly", or "monthly"
    amortization_period: Whole number between 5 and 25 inclusive

    Returns a json object with the key "maximum_mortgage" and the maximum amount of the mortgage

PATCH /interest-rate

    Params:
    interest_rate: A percentage value greater than 0.

    Updates the internal interest rate used by the calculator.
    Note: Changes made via this endpoint do not persist if the API
    is shut down.

The API is written using the python library starlette and can be run using uvicorn with the command:
uvicorn api:app --reload
from the /app directory.