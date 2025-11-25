import re

def extract_strings(filename, min_len=4):
    with open(filename, 'rb') as f:
        data = f.read()
    # Regex to find sequences of printable characters
    # 32-126 are printable ASCII
    pattern = re.compile(b'[ -~]{' + str(min_len).encode() + b',}')
    for match in pattern.finditer(data):
        try:
            print(match.group().decode('utf-8'))
        except:
            pass

if __name__ == "__main__":
    extract_strings("ECS 235A Project Report-1.pdf", min_len=10)
