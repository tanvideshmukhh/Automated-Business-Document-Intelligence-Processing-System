import re


def clean_text(value):
    """Remove extra spaces and normalize text."""

    if value is None:
        return ""

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_currency(currency):
    """Convert different currency representations to INR."""

    if not currency:
        return ""

    currency = clean_text(currency).upper()

    currency_map = {
        "₹": "INR",
        "RS": "INR",
        "RS.": "INR",
        "INR": "INR",
        "IND": "INR",
        "INDIA": "INR",
        "$": "USD",
        "USD": "USD"
    }

    return currency_map.get(currency, currency)


def normalize_category(category):
    """Normalize expense categories."""

    if not category:
        return ""

    category = clean_text(category).lower()

    category_map = {
        "software": "Software",
        "software & services": "Software",
        "travel": "Travel",
        "food": "Food",
        "transport": "Transport",
        "office": "Office",
        "medical": "Medical",
        "accommodation": "Accommodation"
    }

    return category_map.get(
        category,
        category.title()
    )


def normalize_amount(amount):
    """Convert monetary values into float."""

    if amount is None:
        return None

    try:
        amount = str(amount)

        # Remove currency symbols and commas
        amount = amount.replace("₹", "")
        amount = amount.replace("INR", "")
        amount = amount.replace(",", "")
        amount = amount.strip()

        return float(amount)

    except ValueError:
        return None


def clean_record(record):
    """Clean all values in a record."""

    cleaned = {}

    for key, value in record.items():

        if "amount" in key or "price" in key:
            cleaned[key] = normalize_amount(value)

        elif key == "currency":
            cleaned[key] = normalize_currency(value)

        elif key == "category":
            cleaned[key] = normalize_category(value)

        else:
            cleaned[key] = clean_text(value)

    return cleaned


if __name__ == "__main__":

    sample_data = {
        "vendor_name": "  TechNova   Solutions ",
        "currency": "₹",
        "total_amount": "₹47,200",
        "category": " SOFTWARE "
    }

    print("Before Cleaning:")
    print(sample_data)

    cleaned_data = clean_record(sample_data)

    print("\nAfter Cleaning:")
    print(cleaned_data)