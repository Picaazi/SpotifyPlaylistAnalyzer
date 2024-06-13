def delete_words_from_file(input_file, output_file, words_to_delete):
    # Read the input file
    with open(input_file, 'r') as f:
        text = f.read()

    # Remove specific words
    for word in words_to_delete:
        text = text.replace(word, ',')

    # Write back to the output file
    with open(output_file, 'w') as f:
        f.write(text)

# Input and output path
input_file = 'CountryCodeOutput.txt'  # Replace with your input file path
output_file = 'CountryCodeOutput2.txt'  # Replace with your output file path

# Words to delete
words_to_delete = ['  ']

# Call the function
delete_words_from_file(input_file, output_file, words_to_delete)

print(f'Specific words removed from {input_file} and saved to {output_file}.')
