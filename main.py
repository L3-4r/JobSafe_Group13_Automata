from symbol_mapper import SymbolMapper
from pda_validator import PDAValidator

def main():
    # 1. Initialize System
    mapper = SymbolMapper()
    pda = PDAValidator()

    # 2. Input Data (A "Strictly Correct" Contract Example)
    # ORDER: Header -> Role -> Term -> Scope -> Pay -> Benefits -> Legal -> Termination -> Sign
    raw_contract_text = """
    KNOW ALL MEN BY THESE PRESENTS:
    This Contract of Employment is entered into by the Company and the Employee.

    Position:
    The Employee is hired as a Junior Developer.

    Term of Employment:
    The start date is January 20, 2026.

    Scope of Work:
    1. Debug legacy code.
    2. Write documentation.

    Compensation:
    The Basic Pay shall be 25,000 PHP per month.

    Benefits:
    The employee receives 13th Month Pay.

    Confidentiality:
    The employee agrees to keep trade secrets confidential.

    Termination:
    Either party may terminate this agreement with notice.

    Signatures:
    Signed: ____________________
    """

    print("--- STEP 1: PREPROCESSING (Symbol Mapping) ---")
    lines = raw_contract_text.strip().split('\n')
    token_stream = []

    for line in lines:
        symbol = mapper.get_symbol(line)
        if symbol:
            print(f"Found: {symbol} | Line: {line.strip()[:30]}...")
            token_stream.append(symbol)
    
    print(f"\nFinal Token Stream: {token_stream}")

    # 3. Validate
    print("\n--- STEP 2: PDA VALIDATION ---")
    is_valid, log = pda.validate(token_stream)

    # 4. Output Results
    print("\n" + "="*30)
    if is_valid:
        print("RESULT: CONTRACT ACCEPTED (Valid Structure)")
    else:
        print("RESULT: CONTRACT REJECTED (Invalid Structure)")
    print("="*30)
    
    print("\n--- SYSTEM LOG (For Debugging) ---")
    for entry in log:
        print(entry)

if __name__ == "__main__":
    main()