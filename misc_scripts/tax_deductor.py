from currency_converter import CurrencyConverter


cc = CurrencyConverter()


def gods_blessing(amount: int, tax_rate:int) -> str:
    discount = (tax_rate / 100) * amount
    result = amount - discount
    amt_usd = cc.convert(amount, "MXN", "USD")
    net_amt_usd = cc.convert(result, "MXN", "USD")
    print(f"Gross Amount (USD): ${int(amt_usd):,}")
    print(f"Gross Amount (MXN): ${amount:,}")
    print(f"40% Tax Discount: ${int(discount):,}")
    print(f"Net Amount (USD): ${int(net_amt_usd):,}")
    net_part = divide_income_one_payout(result)
    net_part_30 = divide_income_30_year_payout(result)
    payouts = [net_part, net_part_30]
    for payout in payouts:
        print(payout)

    return "God is great!"


def discount_charity(income):
    """10% off the income for charity."""
    return (10 / 100) * income


def divide_income_one_payout(income: float, divider=3):
    """
    Divide the income into 3 parts, following the Jewish tradition and giving 10% of the income to charity.
    """
    charity_disc = int(discount_charity(income))
    d_income = int(income - charity_disc)
    part = int(d_income / divider)
    usd_net_income = cc.convert(income, "MXN", "USD")
    usd_part = cc.convert(part, "MXN", "USD")

    return f"""
    ---One payout---
    Net income: ${int(income):,}
    Net income in USD: ${int(usd_net_income):,}
    10% Charity: ${charity_disc:,}
    ==== After Charity ====
    Part in USD: ${int(usd_part):,}
    Live Part: ${part:,}
    Investment Part: ${int(part):,}
    Gold Part: ${part:,}
    """


def divide_income_30_year_payout(income: float, divider=3):
    """
    Divide the income into 30 parts, following the Jewish tradition and giving 10% of the income to charity.
    """
    charity_disc = int(discount_charity(income))
    yearly_charity_disc = int(charity_disc / 30)
    usd_net_income = cc.convert(income, "MXN", "USD")
    d_income = int(income - charity_disc)
    yearly_part = int(d_income / 30)
    usd_yearly_part = cc.convert(yearly_part, "MXN", "USD")
    part = int(yearly_part / divider)
    usd_part = cc.convert(part, "MXN", "USD")

    return f"""
    ---30 year payout---
    Net income: ${int(income):,}
    Net income in USD: ${int(usd_net_income):,}
    10% Charity: ${charity_disc:,}
    Yearly Charity: ${yearly_charity_disc:,}
    ==== After Charity ====
    Yearly Part: ${yearly_part:,}
    Yearly Part in USD: ${int(usd_yearly_part):,}
    Part in USD: ${int(usd_part):,}
    Live Part: ${part:,}
    Investment Part: ${part:,}
    Gold Part: ${part:,}
    """


if __name__ == "__main__":
    print(gods_blessing(15_900_000_000, 40))
