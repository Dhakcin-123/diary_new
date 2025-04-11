from datetime import datetime

DIARY_FILE = "Diary.txt"
count = 0

def save_entry(entry,category):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(DIARY_FILE,"a") as f:
        f.write(f"[{timestamp}] [{category}] {entry}\n")
    print("Entry saved")

def read_entries(filter_category = None,filter_date = None):
    try:
        with open(DIARY_FILE,"r") as f:
            lines = f.readlines()
        if not lines:
            print("No entries yet")
            return
        print("\nYour diary entries")
        found = False
        for line in lines:
            if "[" in line and "]" in line:
                timestamp_end = line.index("]")+1
                category_end = line.index("]",timestamp_end)+1
                timestamp = line[1:timestamp_end-1]
                category = line[timestamp_end+2:category_end-1]
                entry = line[category_end+1:].strip()
                date_match = (filter_date is None or timestamp.startswith(filter_date))
                category_match = (filter_category is None or category.lower() == filter_category.lower())
                if date_match and category_match:
                    print(f"[{timestamp}] [{category}] {entry}")
                    found = True
        if not found:
            print("No matching entries found")
    except FileNotFoundError:
        print("No diary file yet")

def delete_entry(timestamp):
    try:
        with open(DIARY_FILE,"r") as f:
            lines = f.readlines()
        if not lines:
            print("No entries to delete")
            return
        new_lines = [line for line in lines if not line.startswith(f"[{timestamp}]")]
        with open(DIARY_FILE,"w") as f:
            f.writelines(new_lines)
        if len(new_lines) < len(lines):
            print("Entry deleted")
        else:
            print("No entry found with that timestamp")
    except FileNotFoundError:
        print("No diary file yet")

print("Welcome to your Diary app")
print("Options:'Write', 'Read', 'Search', 'Delete', 'Quit', 'Count'")
while True:
    choice = input("What dou you want to do:").lower().strip()
    if choice == "quit":
        print("See you later")
        break
    elif choice == "write":
        entry = input("Write your diary entry: ").strip()
        category = input("Enter a category (example: Work or personal): ")
        count = count+1
        save_entry(entry,category)
    elif choice == "read":
        category_filter = input("Filter by category or enter for all: ").strip() or None
        read_entries(category_filter)
    elif choice == "search":
        date_filter = input("Enter date to search (yyyy-mm-dd): ").strip()
        if len(date_filter) != 10 or date_filter[4] != "-" or date_filter[7] != "-":
            print("Invalid date format. Use (yyyy-mm-dd)")
        else:
            read_entries(filter_date = date_filter)
    elif choice == "delete":
        timestamp = input("Enter exact timestamp to delete (yyyy-mm-dd HH:MM)").strip()
        delete_entry(timestamp)
    elif choice == "count":
        print(count,"Entry has been entered")    
    else:
        print("Invalid option")