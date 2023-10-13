import re
import pandas as pd

# Regular expression pattern to match the timestamp, sender, and message
pattern = r'\[(.*?)\] (.*?): (.*)'

# Path to the input text file
input_file = 'input.txt'

# Path to the output Excel file
output_file = 'output.xlsx'

# Read the input text file
with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Initialize lists to store the extracted data
timestamps = []
senders = []
messages = []

# Initialize variables to track the current message
current_timestamp = None
current_sender = None
current_message = ''

# Process each line and extract the timestamp, sender, and message
for line in lines:
    match = re.match(pattern, line)
    if match:
        # Save the previous message, if any
        if current_timestamp and current_sender and current_message:
            timestamps.append(current_timestamp)
            senders.append(current_sender)
            messages.append(current_message.strip())

        # Start a new message
        current_timestamp = match.group(1)
        current_sender = match.group(2)
        current_message = match.group(3)
    else:
        # Append the line to the current message with a space
        current_message += ' ' + line.strip()

# Save the last message
if current_timestamp and current_sender and current_message:
    timestamps.append(current_timestamp)
    senders.append(current_sender)
    messages.append(current_message.strip())

# Create a DataFrame from the extracted data
data = {
    'Timestamp': timestamps,
    'Sender': senders,
    'Message': messages
}
df = pd.DataFrame(data)

# Save the DataFrame to Excel
df.to_excel(output_file, index=False)
