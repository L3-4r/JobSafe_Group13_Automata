import re

class SymbolMapper:
    def __init__(self):
        # 1. Define Rules with Regex Boundaries
        # r'' indicates a raw string, essential for regex patterns.
        self.rules = {
            'H': [r'employment agreement', r'contract of employment', r'know all men', r'service agreement', r'letter of offer'],
            'R': [r'position', r'job title', r'designation', r'hired as', r'\brank\b'], # \b prevents matching 'frank'
            'D': [r'term of employment', r'effective date', r'probationary', r'start date', r'period of employment', r'\bduration\b'], 
            'S': [r'duties', r'responsibilities', r'functions', r'deliverables', r'scope of work', r'obligations', r'job description'],
            'C': [r'basic pay', r'monthly rate', r'gross salary', r'remuneration', r'hourly rate', r'compensation', r'\bsalary\b'],
            'B': [r'allowance', r'13th month', r'hmo', r'incentives', r'sss', r'philhealth', r'pag-ibig', r'insurance', r'benefits'],
            'F': [r'confidentiality', r'non-disclosure', r'data privacy', r'proprietary', r'intellectual property'],
            'T': [r'resignation', r'termination', r'notice period', r'breach', r'separation', r'end of contract'],
            'X': [r'signed', r'witness', r'conforme', r'accepted by', r'signature']
        }

    def get_symbol(self, line):
        clean_line = line.strip().lower()
        if not clean_line:
            return None

        # Logic Patch: Limit search scope for very long lines
        # This prevents finding a keyword that appears casually at the end of a long sentence.
        search_text = clean_line
        words = clean_line.split()
        if len(words) >= 20:
            search_text = " ".join(words[:15])

        for symbol, patterns in self.rules.items():
            for pattern in patterns:
                # re.search scans the string for the pattern
                # re.IGNORECASE makes it case-insensitive
                if re.search(pattern, search_text, re.IGNORECASE):
                    return symbol
        
        return None

# --- Quick Test Block ---
# You can run this file directly to test it: 'python symbol_mapper.py'
if __name__ == "__main__":
    mapper = SymbolMapper()
    
    test_lines = [
        "Frankly, I think this is a good idea.",       # Should be None (previously matched 'rank' -> R)
        "The Position is Junior Dev",                 # Should be R
        "This contract has a long term duration.",    # Should be D
        "We need strictly confidential treatment."    # Should be F
    ]

    print("--- Testing Symbol Mapper v2.0 ---")
    for line in test_lines:
        token = mapper.get_symbol(line)
        print(f"Input: '{line}' -> Detected: {token}")