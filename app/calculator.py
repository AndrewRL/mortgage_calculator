from math import modf

class MortgageCalculator:
    def __init__(self):
        self.interest_rate = .025
        self.annual_payments = {
            'weekly': 52,
            'biweekly': 26,
            'monthly': 12
        }
        self.insurance_tiers = [
            {'min': .05, 'max': .0999, 'rate': .0315},
            {'min': .1, 'max': .1499, 'rate': .024},
            {'min': .15, 'max': .1999, 'rate': .018},
            {'min': .2, 'max': 1.00, 'rate': 0}
        ]
        self.insurable_limit = 1000000
        self.minimum_amortization_period = 5
        self.maximum_amortization_period = 25
        self.param_dtypes = {
            'asking_price': float,
            'down_payment': float,
            'payment_schedule': str,
            'amortization_period': int,
            'payment': float
        }


    def payment_per_period(self, asking_price, down_payment, payment_schedule, amortization_period):
        if down_payment < minimum_down_payment(asking_price):
            return DeclinedMortgage(f'The minimum down payment for an asking price of ${asking_price} is ${minimum_down_payment(asking_price)}.')

        principal = asking_price - down_payment
        if self.insurable_limit < principal and down_payment_percentage(asking_price, down_payment) < .2:
            return DeclinedMortgage(f'You must make a down payment of at least 20% on mortgages over ${self.insurable_limit}.')

        principal += calculate_insurance_cost(self.insurance_tiers, asking_price, down_payment)
        annual_payments = self.annual_payments[payment_schedule]
        n_payments = annual_payments * amortization_period

        payment_per_period = round(calculate_payment(principal, self.interest_rate, annual_payments, n_payments), 2)
        return ApprovedMortgage(payment_per_period)

    def maximum(self, payment_amount, payment_schedule, amortization_period):
        
        annual_payments = self.annual_payments[payment_schedule]

        principal = payment_amount * annual_payments * amortization_period

        return principal


class Mortgage:
    def __init__(self, status=None, status_text=''):
        self.status = status
        self.status_text = status_text


class DeclinedMortgage(Mortgage):
    def __init__(self, status_text='You cannot create a mortgage with the given parameters.'):
        super().__init__('declined', status_text)


class ApprovedMortgage(Mortgage):
    def __init__(self, payment_per_period):
        super().__init__('approved', 'The mortgage was approved.')
        self.payment_per_period = payment_per_period


class Money:
    def __init__(self, amount):
        whole, part = modf(amount)
        whole = int(whole)
        part = int(round(part, 2) * 100)
        self.dollars = whole
        self.cents = part


def calculate_payment(principal, interest_rate, annual_payments, total_payments):
    period_interest_rate = interest_rate / annual_payments
    return principal * ((period_interest_rate*(1+period_interest_rate)**total_payments) / ((1 + period_interest_rate)**total_payments - 1))


def calculate_insurance_cost(insurance_tiers, asking_price, down_payment):

    down_payment_pct = down_payment_percentage(asking_price, down_payment)
    insurance_rate = None
    for tier in insurance_tiers:
        if tier['min'] <= down_payment_pct <= tier['max']:
            insurance_rate = tier['rate']
            break

    if insurance_rate is None:
        raise ValueError('The down payment percentage is not in any configured insurance tier.')

    return asking_price * insurance_rate


def minimum_down_payment(asking_price):
        if asking_price <= 500000:
            return asking_price * .05
        elif asking_price > 500000:
            return  500000 * .05 + (asking_price - 500000) * .1


def down_payment_percentage(asking_price, down_payment):
        return round(down_payment / asking_price, 4)

