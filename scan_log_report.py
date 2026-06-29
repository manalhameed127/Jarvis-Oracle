from src.scan_logger import load_scan_log


def main():
    log_entries = load_scan_log()

    print("\nSCAN LOG REPORT")
    print("=" * 50)
    print("Total Scan Entries:", len(log_entries))

    if not log_entries:
        print("No scan entries yet.")
        return

    print("\nLast 10 Entries:")
    for entry in log_entries[-10:]:
        print()
        print("Time:", entry["created_at"])
        print("Symbol:", entry["symbol"])
        print("Status:", entry["status"])
        print("Reason:", entry["reason"])
        print("Score:", entry["score"])
        print("Decision:", entry["decision"])
        print("Pattern:", entry["pattern_prediction"])


if __name__ == "__main__":
    main()
