import hashlib
import os


def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception as e:
        return None


def compare_records(record1, record2):
    """
    Compare two structured records and identify
    possible duplicate indicators.
    """

    matches = []

    if (
        record1.get("invoice_number")
        and record1.get("invoice_number")
        == record2.get("invoice_number")
    ):
        matches.append("Same invoice number")

    if (
        record1.get("vendor_name")
        and record1.get("vendor_name").lower()
        == record2.get("vendor_name", "").lower()
    ):
        matches.append("Same vendor")

    if (
        record1.get("invoice_date")
        and record1.get("invoice_date")
        == record2.get("invoice_date")
    ):
        matches.append("Same document date")

    if (
        record1.get("total_amount") is not None
        and record1.get("total_amount")
        == record2.get("total_amount")
    ):
        matches.append("Same total amount")

    if (
        record1.get("po_number")
        and record1.get("po_number")
        == record2.get("po_number")
    ):
        matches.append("Same PO number")

    return matches


def is_potential_duplicate(record1, record2):
    """Determine whether two records are potential duplicates."""

    matches = compare_records(record1, record2)

    # Strong duplicate indicators
    strong_indicators = [
        "Same invoice number",
        "Same PO number"
    ]

    if any(indicator in matches for indicator in strong_indicators):
        return True, matches

    # Multiple matching fields also indicate a potential duplicate
    if len(matches) >= 3:
        return True, matches

    return False, matches


def find_duplicate_records(records):
    """
    Compare all records and return potential duplicates.
    """

    duplicates = []

    for i in range(len(records)):
        for j in range(i + 1, len(records)):

            is_duplicate, matches = is_potential_duplicate(
                records[i],
                records[j]
            )

            if is_duplicate:
                duplicates.append({
                    "record_1": i,
                    "record_2": j,
                    "matching_indicators": matches
                })

    return duplicates


if __name__ == "__main__":

    record1 = {
        "vendor_name": "TechNova Solutions",
        "invoice_number": "INV-20481",
        "invoice_date": "18/08/2026",
        "total_amount": 47200
    }

    record2 = {
        "vendor_name": "TechNova Solutions",
        "invoice_number": "INV-20481",
        "invoice_date": "18/08/2026",
        "total_amount": 47200
    }

    record3 = {
        "vendor_name": "Another Company",
        "invoice_number": "INV-30001",
        "invoice_date": "20/08/2026",
        "total_amount": 15000
    }

    records = [record1, record2, record3]

    duplicates = find_duplicate_records(records)

    print("Duplicate Detection Module")
    print("=" * 40)

    if duplicates:
        print("Potential duplicates found:")

        for duplicate in duplicates:
            print(
                f"Record {duplicate['record_1']} "
                f"and Record {duplicate['record_2']}"
            )

            print(
                "Matching indicators:",
                ", ".join(
                    duplicate["matching_indicators"]
                )
            )

    else:
        print("No potential duplicates found.")