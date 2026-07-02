from datetime import datetime , timezone
from time import sleep

class Transaction:
    def __init__(self, amount, tx_type, timestamp):
        self.amount = amount
        self.type = tx_type
        self.timestamp = timestamp

    def __eq__(self, other):
        return (
            self.amount == other.amount and
            self.type == other.type and
            self.timestamp == other.timestamp
        )

class LedgerWallet:
    def __init__(self):
        self.ledgers = {}
    
    def add_transaction(self, currency, amount, tx_type):
        current_utc = datetime.now(timezone.utc)
        timestamp = current_utc.isoformat()

        if currency not in self.ledgers:
            self.ledgers[currency] = []
        self.ledgers[currency].append(Transaction(amount=amount, tx_type=tx_type, timestamp=timestamp))
    
    def get_balance(self, currency):
        total = 0
        try:
            if not isinstance(currency, str):
                raise TypeError(f"Please Enter the Correct Currency (USD/INF):- X{currency}X")
            if currency.upper() not in self.ledgers:
                raise ValueError(f"NO SUCH CURRENCY EXIST:- TRY AGAIN!!!!")
        except (TypeError, ValueError) as error_msg:
            return f"App Error:- {error_msg}"
        
        transactions = self.ledgers.get(currency.upper(), [])
        for transaction in transactions:
            if transaction.type == 'credit':
                total += transaction.amount
            elif transaction.type == 'debit':
                total -= transaction.amount

        return total

    def _create_snapshot(self):
        return {currency: entries[:] for currency, entries in self.ledgers.items()}

    def _restore(self, snapshot):
        self.ledgers = snapshot

    def safe_transaction(self, currency, amount, tx_type, simulate_crash=False):
        snapshot = self._create_snapshot()
        try:
            self.add_transaction(currency=currency, amount=amount, tx_type=tx_type)

            if simulate_crash:
                raise RuntimeError("Simulated crash after write, before confirm")
        except Exception as error_msg:
            self._restore(snapshot=snapshot)
            return f"Transaction Failed. Please try again later...."
        return f"Transaction Successfull"
    
wallet = LedgerWallet()

wallet.safe_transaction(currency='USD', amount=100, tx_type='credit')
print(f"Your Current Balance:- {wallet.get_balance(currency='usd')}")

# ab equality test
t1 = Transaction(100, 'credit', "2026-07-01T10:00:00")
t2 = Transaction(100, 'credit', "2026-07-01T10:00:00")
t3 = Transaction(50, 'debit', "2026-07-01T10:05:00")

print(t1 == t2)   # expect True (same info = duplicate)
print(t1 == t3)   # expect False (different info)

wallet.safe_transaction(currency='USD', amount=50, tx_type='debit', simulate_crash=True)
print(f"Your Current Balance:- {wallet.get_balance(currency='usd')}")