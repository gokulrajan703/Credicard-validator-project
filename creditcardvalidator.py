import datetime

def clean_card_number(card_number):
    """Remove spaces and dashes, check if numeric"""
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit():
        raise ValueError("Card number must contain only digits, spaces, or dashes.")
    return card_number

def get_card_type(card_number):
    """Identify basic card types by number prefixes"""
    if card_number.startswith('4'):
        return "Visa"
    elif card_number.startswith(('51', '52', '53', '54', '55')):
        return "MasterCard"
    elif card_number.startswith(('34', '37')):
        return "American Express"
    elif card_number.startswith('6'):
        return "Discover"
    else:
        return "Unknown"

def valid_check(card_number):
    sum_odd_digits = 0
    sum_even_digits = 0
    card_number = card_number[::-1]

    # Odd-position digits
    for x in card_number[::2]:
        sum_odd_digits += int(x)

    # Even-position digits
    for x in card_number[1::2]:
        x = int(x) * 2
        sum_even_digits += x if x < 10 else (1 + (x % 10))

    total = sum_odd_digits + sum_even_digits
    return total % 10 == 0

def validate_expiry_date(expiry):
    """Validate MM/YY format and check if it's not expired"""
    try:
        month, year = expiry.split("/")
        if len(year) == 2:
            year = "20" + year  # Convert to 4-digit year
        month = int(month)
        year = int(year)
        if month < 1 or month > 12:
            return False, "Invalid expiry month."

        now = datetime.datetime.now()
        expiry_date = datetime.datetime(year, month, 1)

        # Compare with the current month
        if expiry_date < now.replace(day=1):
            return False, "Card is expired."

        return True, "Valid expiry date."
    except ValueError:
        return False, "Invalid format. Use MM/YY."

def validate_card(card_number, expiry_date):
    try:
        card_number = clean_card_number(card_number)
    except ValueError as e:
        return str(e)

    expiry_valid, expiry_msg = validate_expiry_date(expiry_date)
    if not expiry_valid:
        return f"INVALID expiry date: {expiry_msg}"

    is_valid = valid_check(card_number)
    card_type = get_card_type(card_number)

    if is_valid:
        return f"VALID {card_type} card.\n{expiry_msg}"
    else:
        return "INVALID card number."

# Run the validator
card_number = input("Enter credit card number: ")
expiry_date = input("Enter expiry date (MM/YY): ")
result = validate_card(card_number, expiry_date)
print(result)
