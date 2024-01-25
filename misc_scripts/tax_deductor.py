def deduct_tax(amount, tax_rate):
    discount = (tax_rate / 100) * amount
    result = amount - discount
    return f"${result:,}"


if __name__ == "__main__":
    print(deduct_tax(304_200_000, 16))
