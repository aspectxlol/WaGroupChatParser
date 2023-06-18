import datetime
import re
import csv
import argparse
import sys
from tqdm import tqdm

GREEN = "\033[92m"


def custom_split(message: str):
    new_message = message.split(" - ", 1)[1]
    return new_message.split(": ")


def check_if_current_line_is_new_line_current_line_being_the_passed_argument(line):
    if re.match(r'^\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\u202F[AP]M\s-\s.+$', line):
        return True
    else:
        return False


data = [["Time", "user", "action", "content"]]


def processMessage(message: str):
    # 8/22/22, 10:02 PM - Epan: Dia gada merendah
    time = message.split(" - ", 1)[0]
    time = datetime.datetime.strptime(time, "%m/%d/%y, %I:%M %p")

    message_after_split = custom_split(message)
    if len(message_after_split) > 1:
        user = message_after_split[0]
        content = message_after_split[1]
        action = "MessageEvent"
    else:
        user = message_after_split[0].split(" ")[0]
        action = message_after_split[0]
        content = None

    data.append([f'{time}', user, action, content])

    return time, user, action, content


def printingMessage(message: object):
    # print(message[1])
    print(f'time: {message[0]}')
    print(f'user: {message[1]}')
    print(f'action: {message[2]}')
    print(f'content: {message[3]}')
    print("")
    return True


def main(filepath, exportPath):
    messages = []
    with open(filepath, 'r', encoding="utf-8") as file:
        messages = file.read()
        messages = messages.split('\n')

    merged_lines = ""
    with tqdm(total=len(messages), unit="messages") as pbar:
        for i, line in enumerate(messages):
            if check_if_current_line_is_new_line_current_line_being_the_passed_argument(line):
                merged_lines = line
                if i+1 < len(messages):
                    if (check_if_current_line_is_new_line_current_line_being_the_passed_argument(messages[i+1])):
                        processMessage(merged_lines)
                else:
                    processMessage(merged_lines)
            else:
                merged_lines += " " + line
                if (i+1) < len(messages):
                    if check_if_current_line_is_new_line_current_line_being_the_passed_argument(messages[i+1]):
                        processMessage(merged_lines)
                else:
                    processMessage(merged_lines)
        pbar.update(1)

    with open(exportPath, 'w', newline='') as file:
        writter = csv.writer(file)
        writter.writerows(data)
        print(f"{GREEN} Sucessfully Parsed a lot of mesages :D")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse a whatsapp groupchat")
    parser.add_argument(
        "-i", "--input", help="Path to the input file.", required=True)
    parser.add_argument(
        "-o", "--output", help="Path to the output file.", required=True)
    args = parser.parse_args()
    input_file_path = args.input
    output_file_path = args.output

    # Check if the required arguments are provided
    if input_file_path is None or output_file_path is None:
        print("Both input and output file paths are required.")
        sys.exit(1)

    # Check file extensions
    if not input_file_path.lower().endswith('.txt'):
        print("Input file must have a .txt extension.")
        sys.exit(1)

    if not output_file_path.lower().endswith('.csv'):
        print("Output file must have a .csv extension.")
        sys.exit(1)
    main(args.input, args.output)
