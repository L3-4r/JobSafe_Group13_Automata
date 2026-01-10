import re

class SymbolMapper:
    def __init__(self):
        # 1. Define the Dictionary
        self.rules = {
            
            'H': ['employment agreement', 'contract of employment', 'know all men', 'service agreement', 'letter of offer'],
            
            'R': ['position', 'job title', 'designation', 'hired as', 'rank'],
            
            'D': ['term of employment', 'effective date', 'probationary', 'start date', 'period of employment', 'duration'], 
            
            'S': ['duties', 'responsibilities', 'functions', 'deliverables', 'scope of work', 'obligations', 'job description'],
            
            'C': ['basic pay', 'monthly rate', 'gross salary', 'remuneration', 'hourly rate', 'compensation', 'salary'],
            
            'B': ['allowance', '13th month', 'hmo', 'incentives', 'sss', 'philhealth', 'pag-ibig', 'insurance', 'benefits'],
            
            'F': ['confidentiality', 'non-disclosure', 'data privacy', 'proprietary', 'intellectual property'],
            
            'T': ['resignation', 'termination', 'notice period', 'breach', 'separation', 'end of contract'],
            
            'X': ['signed', 'witness', 'conforme', 'accepted by', 'signature']
        }

    def get_symbol(self, line):
        """
        Scans a line of text and returns the corresponding Symbol (Token).
        Returns None if the line is 'noise'.
        """
        clean_line = line.strip().lower()
        if not clean_line:
            return None

        words = clean_line.split()
        
        #discrepany filter (temporary)
        target_text = clean_line 
        
        # Only truncate if it's REALLY long to capture keywords mid-sentence
        if len(words) >= 20: 
            target_text = " ".join(words[:15])

        for symbol, keywords in self.rules.items():
            for keyword in keywords:
              
                if keyword in target_text:
                    return symbol
        
        return None
# Quick Test Block
if __name__ == "__main__":
    mapper = SymbolMapper()
    
    test_lines = [
        "Republic of the Philippines",                     # Noise (None)
        "CONTRACT OF EMPLOYMENT",                          # Header (H)
        "The position you are hired as is Software Dev.",  # Role (R)
        "The employee must maintain confidentiality.",     # Confidentiality (F) - Short line
        "The employee understands that the nature of the work requires strict confidentiality regarding data." # Long line (Should be Noise/None because 'confidentiality' is late)
    ]

    print("--- Testing Symbol Mapper ---")
    for line in test_lines:
        token = mapper.get_symbol(line)
        print(f"'{line[:30]}...' -> {token}")
