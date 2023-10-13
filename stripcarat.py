# Path to the input text file
input_file = 'input.txt'

# Path to the output text file
output_file = 'output_stripped.txt'

# Read the input text file
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Remove angle brackets from the content
stripped_content = content.replace('<', '').replace('>', '')

# Write the stripped content back to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(stripped_content)

print("Angle brackets stripped and content saved to", output_file)
