import json
import string

with open('lines.json', 'r') as f:
    lines = json.load(f)

modern = []
original = []
for line in lines:
    modern.append(line['modern'])
    original.append(line['original'])

table = str.maketrans('', '', string.punctuation)

modern = " ".join(modern)
modern = modern.split(" ")
modern = [word.translate(table).lower() for word in modern]

original = " ".join(original)
original = original.split(" ")
original = [word.translate(table).lower() for word in original]

print(f'len(modern): {len(set(modern))}\nlen(original): {len(set(original))}')
