from datetime import datetime


def validate_date(date_string):
    """Check whether a date is valid."""

    if not date_string:
        return False

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d %B %Y",
        "%d %b %Y"
    ]

    for date_format in formats:
        try:
            datetime.strptime(date_string.strip(), date_format)
            return True
        except ValueError:
            continue

    return False


def validate_amount(amount):
    """Check whether an amount is numeric and non-negative."""

    try:
        amount = float(amount)
        return amount >= 0
    except (ValueError, TypeError):
        return False


def validate_invoice(data):
    """Validate invoice information."""

    errors = []

    required_fields = [
        "vendor_name",
        "invoice_number",
        "invoice_date",
        "currency",
        "total_amount"
    ]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    if data.get("invoice_date"):
        if not validate_date(data["invoice_date"]):
            errors.append("Invalid invoice date")

    if data.get("due_date"):
        if not validate_date(data["due_date"]):
            errors.append("Invalid due date")

    if data.get("total_amount") is not None:
        if not validate_amount(data["total_amount"]):
            errors.append("Invalid or negative total amount")

    return errors


def validate_purchase_order(data):
    """Validate purchase order information."""

    errors = []

    required_fields = [
        "po_number",
        "vendor_name",
        "order_date",
        "quantity",
        "unit_price",
        "total_amount"
    ]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    if data.get("order_date"):
        if not validate_date(data["order_date"]):
            errors.append("Invalid order date")

    if data.get("delivery_date"):
        if not validate_date(data["delivery_date"]):
            errors.append("Invalid delivery date")

    if data.get("quantity") is not None:
        try:
            if float(data["quantity"]) <= 0:
                errors.append("Quantity must be positive")
        except (ValueError, TypeError):
            errors.append("Invalid quantity")

    if data.get("unit_price") is not None:
        if not validate_amount(data["unit_price"]):
            errors.append("Invalid unit price")

    if data.get("total_amount") is not None:
        if not validate_amount(data["total_amount"]):
            errors.append("Invalid total amount")

    return errors


def validate_expense(data):
    """Validate expense statement information."""

    errors = []

    required_fields = [
        "employee_name",
        "employee_id",
        "department",
        "expense_date",
        "category",
        "amount",
        "currency"
    ]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    if data.get("expense_date"):
        if not validate_date(data["expense_date"]):
            errors.append("Invalid expense date")

    if data.get("amount") is not None:
        if not validate_amount(data["amount"]):
            errors.append("Invalid or negative expense amount")

    accepted_categories = [
        "travel",
        "food",
        "accommodation",
        "office",
        "software",
        "transport",
        "medical",
        "other"
    ]

    if data.get("category"):
        category = data["category"].strip().lower()

        if category not in accepted_categories:
            errors.append(
                f"Invalid expense category: {data['category']}"
            )

    return errors


def validate_document(document_type, data):
    """Select the correct validator."""

    if document_type == "Invoice":
        errors = validate_invoice(data)

    elif document_type == "Purchase Order":
        errors = validate_purchase_order(data)

    elif document_type == "Expense Statement":
        errors = validate_expense(data)

    else:
        errors = ["Unknown document type"]

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


if __name__ == "__main__":

    print("Validator Module")
    print("=" * 40)

    sample_invoice = {
        "vendor_name": "TechNova Solutions",
        "invoice_number": "INV-20481",
        "invoice_date": "18/08/2026",
        "currency": "INR",
        "total_amount": 47200
    }

    result = validate_document(
        "Invoice",
        sample_invoice
    )

    print("Sample Invoice Validation:")
    print(result)