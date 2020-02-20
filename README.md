Mortgage Calculator API

This API provides the following methods which are useful for calculating mortgage information:

GET /payment-amount\n

Params:\n
asking_price: Whole number or decimal greater than or equal to 0.\n
down_payment: Whole number of decimal greater than or equal to 0 and less than or equal to the asking price.\n
payment_schedule: "weekly", "biweekly", or "monthly"\n
amortization_period: Whole number between 5 and 25 inclusive.\n

Returns a json object with the key "payment_per_period" and the payment amount if the mortgage is allowed.\n
Returns a json object with the keys "mortgage_status" = "declined" and the reason if the mortgage is rejected.\n

GET /mortgage-amount\n

    Params:\n
    payment: Numeric value greater than or equal to 0.\n
    payment_schedule: "weekly", "biweekly", or "monthly"\n
    amortization_period: Whole number between 5 and 25 inclusive\n

    Returns a json object with the key "maximum_mortgage" and the maximum amount of the mortgage\n

PATCH /interest-rate\n

    Params:\n
    interest_rate: A percentage value greater than 0.\n

    Updates the internal interest rate used by the calculator.\n
    Note: Changes made via this endpoint do not persist if the API
    is shut down.

The API is written using the python library starlette and can be run using uvicorn with the command:\n
uvicorn api:app --reload\n
from the /app directory.