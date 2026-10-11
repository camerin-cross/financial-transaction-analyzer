import csv
from collections import defaultdict
from datetime import datetime

CATEGORY_KEYWORDS = {
    "Income": ["paycheck", "deposit"],
    "Groceries": ["kroger", "aldi", "walmart"],
    "Dining": ["chipotle", "starbucks", "mcdonald"],
    "Transport": ["gas", "uber"],
    "Bills": ["electric", "internet", "rent"],
}


def load_transactions(path):
    transactions = []
    with open(path, newline="") as file:
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=2):
            try:
                transactions.append({
                    "date": datetime.strptime(row["date"], "%Y-%m-%d").date(),
                    "description": row["description"],
                    "amount": float(row["amount"]),
                })
            except (ValueError, KeyError):
                print(f"Skipping bad row on line {line_number}: {row}")
    return transactions


def categorize(description):
    text = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return "Other"


def summarize(transactions: list[dict]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for t in transactions:
        month = t["date"].strftime("%Y-%m")
        category = categorize(t["description"])
        summary[month][category] += t["amount"]
    return summary


def print_report(summary: dict[str, dict[str, float]]) -> None:
    for month in sorted(summary):
        print(f"\n=== {month} ===")
        for category, total in sorted(summary[month].items()):
            print(f"{category:<12} {total:>10.2f}")
        net = sum(summary[month].values(), 0.0)
        print(f"{'Net':<12} {net:>10.2f}")


def main():
    try:
        transactions = load_transactions("transactions.csv")
    except FileNotFoundError:
        print("Could not find transactions.csv")
        return
    print_report(summarize(transactions))


if __name__ == "__main__":
    main()