class PDAValidator:
    def __init__(self):
        self.stack = []
        self.current_state = 'q_start'
        self.log = [] 

        # FINAL LOGIC: STRICT SEQUENTIAL DPDA
        # Order: Header -> Role -> Duration -> Scope -> Pay -> Benefits -> Legal -> Term -> Sign
        self.transitions = {
            'q_start': {
                'H': ('q_header', None, None)      
            },
            'q_header': {
                'H': ('q_header', None, None),     # Self-loop (ignore extra headers)
                'R': ('q_role', 'PUSH', 'role_marker') 
            },
            'q_role': {
                'R': ('q_role', None, None),       
                'D': ('q_term', None, None)        
            },
            'q_term': {
                'D': ('q_term', None, None),       
                'S': ('q_scope', 'POP', 'role_marker') # Duties (S) must come after Term
            },
            'q_scope': {
                'S': ('q_scope', None, None),
                'C': ('q_pay_base', 'PUSH', 'pay_marker') # Pay (C) comes AFTER Duties
            },
            'q_pay_base': {
                'C': ('q_pay_base', None, None),
                'B': ('q_benefits', 'POP', 'pay_marker') 
            },
            'q_benefits': {
                'B': ('q_benefits', None, None),
                'F': ('q_legal', None, None)       
            },
            'q_legal': {
                'F': ('q_legal', None, None),
                'T': ('q_term_clause', None, None) 
            },
            'q_term_clause': {
                'T': ('q_term_clause', None, None),
                'X': ('q_accept', None, None)      
            },
            'q_accept': {
                'X': ('q_accept', None, None)      
            }
        }

    def process_token(self, token):
        # 1. Check if the token is valid for the current state
        if token not in self.transitions.get(self.current_state, {}):
            self.log.append(f"REJECT: Unexpected token '{token}' in state '{self.current_state}'. Expected: {list(self.transitions[self.current_state].keys())}")
            return False

        new_state, action, marker = self.transitions[self.current_state][token]

        # 2. Stack Operations
        if action == 'PUSH':
            self.stack.append(marker)
            self.log.append(f"Action: PUSH '{marker}'")
        elif action == 'POP':
            if not self.stack or self.stack[-1] != marker:
                self.log.append(f"REJECT: Dependency Error. Expected to close '{marker}', but stack was {self.stack}.")
                return False
            self.stack.pop()
            self.log.append(f"Action: POP '{marker}'")

        # 3. Transition
        self.current_state = new_state
        return True

    def validate(self, token_stream):
        self.current_state = 'q_start'
        self.stack = []
        self.log = []

        # Fail fast if empty
        if not token_stream:
            return False, ["REJECT: Empty token stream."]

        for token in token_stream:
            if not self.process_token(token):
                return False, self.log 

        # FINAL CHECK: Must be in Accept State AND Stack must be empty
        if self.current_state == 'q_accept' and len(self.stack) == 0:
            return True, self.log
        elif self.current_state != 'q_accept':
            self.log.append(f"REJECT: Contract incomplete. Ended in state '{self.current_state}'.")
            return False, self.log
        elif len(self.stack) > 0:
            self.log.append(f"REJECT: Unresolved dependencies. Stack: {self.stack}")
            return False, self.log