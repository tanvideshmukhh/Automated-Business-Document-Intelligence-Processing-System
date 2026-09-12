import os


def classify_document(filename, text=""):
    """
    Classifies a business document as Invoice,
    Purchase Order, Expense Statement, or Unknown.
    """

    name = filename.lower()
    content = text.lower()

    # Filename-based classification
    if "invoice" in name or "inv" in name:
        return "Invoice"

    if "purchase" in name or "po_" in name or "purchase_order" in name:
        return "Purchase Order"

    if "expense" in name or "expenses" in name:
        return "Expense Statement"

    # Content-based classification
    invoice_keywords = [
        "invoice number",
        "invoice no",
        "invoice #",
        "subtotal",
        "tax amount",
        "grand total"
    ]

    purchase_keywords = [
        "purchase order",
        "po number",
        "order date",
        "expected delivery",
        "unit price"
    ]

    expense_keywords = [
        "employee id",
        "expense category",
        "payment method",
        "expense date"
    ]

    invoice_score = sum(keyword in content for keyword in invoice_keywords)
    purchase_score = sum(keyword in content for keyword in purchase_keywords)
    expense_score = sum(keyword in content for keyword in expense_keywords)

    scores = {
        "Invoice": invoice_score,
        "Purchase Order": purchase_score,
        "Expense Statement": expense_score
    }

    best_type = max(scores, key=scores.get)

    if scores[best_type] > 0:
        return best_type

    return "Unknown"


def get_file_type(filename):
    """Returns the file extension."""

    return os.path.splitext(filename)[1].lower()


if __name__ == "__main__":
    test_files = [
        "invoice_001.pdf",
        "purchase_order_001.pdf",
        "expenses_august.xlsx",
        "random_file.txt"
    ]

    for file in test_files:
        document_type = classify_document(file)
        file_type = get_file_type(file)

        print(f"File: {file}")
        print(f"Extension: {file_type}")
        print(f"Classification: {document_type}")
        print("-" * 40)