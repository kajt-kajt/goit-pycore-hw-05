from sys import argv, exit

"""
Script expects logs of the following format: "YYYY-MM-dd hh:mm:ss LEVEL message"
Example line:

2024-01-22 08:30:01 INFO User logged in successfully.
"""

# List of fields and their corresponding patterns
FIELDS = ["date","time","level","message"]
FORMAT = [
    r"\d{4}-\d{2}-\d{2}",
    r"\d{2}:\d{2}:\d{2}",
    r"\w+",
    r".+"
]

def parse_log_line(line: str) -> dict[str:str]:
    """
    Parses line of logs according to established format.
    If format does not match the pattern, returns empty dict.
    Expected fields and their order are set in global variable FIELDS
    """
    from re import fullmatch
    # splitting to parts by default whitespace chars
    fields_expected = len(FIELDS)
    line_parsed = line.split(maxsplit = fields_expected-1)
    result = {}
    # if there is enough whitespaces to split line according to required format:
    if len(line_parsed)==fields_expected:
        # let's check that each filed matches corresponding pattern in FORMAT global variable
        # list comprehension as required by task
        format_check = [ bool(fullmatch(pattern,field)) for pattern, field in zip(FORMAT, line_parsed)]
        # all function as required by task
        if all(format_check):
            # dictionary comprehension as required by task
            result = {key:value for key, value in zip(FIELDS,line_parsed)}
    return result

def load_logs(file_path: str) -> list[dict]:
    """
    Reads file, parses each line according to format.
    Lines with incorrect format are ignored.
    Outputs list of dictionaries with fields as found in FIELDS
    """
    result = []
    try:
        with open(file_path, "r", encoding = "utf-8") as file:
            for line in file:
                # remove newline at the end and parse log format
                line_parsed = parse_log_line(line[:-1])
                # in case format was recognised:
                if line_parsed:
                    result.append(line_parsed)
    except IOError as e:
        print(f"ERROR opening file \"{file_path}\": {e}")
        # stop further processing, exit with error
        exit(1)
    return result

def filter_logs_by_level(logs: list[dict], level: str) -> list[dict]:
    """
    Given a list of dictionaries with log entries, filter them according to log level.
    """
    level_cleaned = level.casefold()

    def match_level(entry) -> bool:
        entry_level_cleaned = entry["level"].casefold()
        return entry_level_cleaned == level_cleaned

    # filter function and passing function as argument to other function as required by task
    return list(filter(match_level, logs))

def count_logs_by_level(logs: list[dict]) -> dict[str,int]:
    """
    Collect statistics for log entries levels.
    """
    from collections import Counter
    # list comprehension as required by task
    levels_list = [entry["level"] for entry in logs]
    return dict(Counter(levels_list))

def display_log_counts(counts: dict[str:str]):
    """
    Display log levels statistics in a nice table.
    """
    FIRST_COLUMN_WIDTH = 16
    FIRST_HEADER = "Рівень логування"
    SECOND_HEADER = "Кількість"
    print(f"{FIRST_HEADER:<{FIRST_COLUMN_WIDTH}} | {SECOND_HEADER}")
    print("-" * FIRST_COLUMN_WIDTH + "-|-" + "-" * len(SECOND_HEADER))
    for level, quantity in counts.items():
        print(f"{level:<{FIRST_COLUMN_WIDTH}} | {quantity}")

def log_entry_to_str(log_entry:dict[str,str]) -> str:
    """
    Reassemble fields of log entry from dictionary format back to original line.
    """
    # map function and lambda as required by task
    # ensure the correct sequence of fields
    return " ".join(list(map(lambda x: log_entry[x], FIELDS)))

def main():
    if len(argv) == 1:
        print("USAGE HINT: pass log file name as first argument, and log level optionally as second one")
        return
    # first argument is filename
    filename = argv[1]
    logs = load_logs(filename)
    if not logs:
        print("WARNING: Log file is empty or entries format is not correct")
        return
    logs_stats = count_logs_by_level(logs)
    display_log_counts(logs_stats)
    if len(argv) > 2:
        # second argument is log level to view
        required_level = argv[2]
        filtered_logs = filter_logs_by_level(logs,required_level)
        print()
        if filtered_logs:
            for entry in filtered_logs:
                print(log_entry_to_str(entry))
        else:
            print(f"INFO: no logs of level \"{required_level}\" found in \"{filename}\".")

if __name__ == "__main__":
    main()
    