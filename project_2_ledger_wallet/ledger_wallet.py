from datetime import datetime , timezone
from copy import deepcopy

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

class BalanceCalculator:
    positive = lambda amount: amount
    negative = lambda amount: -amount

    TYPE_RULE = {
        "credit" : positive,
        'debit'  : negative
    }
    def calculate(self, transactions):
        total = 0
        for transaction in transactions:
            rule = self.TYPE_RULE.get(transaction.type)
            try:
                if rule is None:
                    raise ValueError(f"Unknown transaction type: {transaction.type}")
            except ValueError as error_msg:
                return "Please Enter the Correct Transcation Type."
            total += rule(transaction.amount)
        return total
    
class BackupRestore:
    def create_snapshot(self, ledgers):
        return deepcopy(ledgers)

    def restore(self, snapshot):
        return snapshot

class LedgerStore:
    def __init__(self):
        self.ledgers = {}
    
    def add_transaction(self, currency, amount, tx_type):
        current_utc = datetime.now(timezone.utc)
        timestamp = current_utc.isoformat()

        if currency not in self.ledgers:
            self.ledgers[currency] = []
        self.ledgers[currency].append(Transaction(amount=amount, tx_type=tx_type, timestamp=timestamp))

class CurrencyValidator:
    def validate(self, currency, currency_list):
        if not isinstance(currency, str):
            raise TypeError(f"Currency must be a string, got: {currency}")
        if currency.upper() not in currency_list:
            raise ValueError(f"Currency '{currency}' does not exist")

class LedgerWallet:
    def __init__(self, calculator, backup_restore, ledger_store, currency_validator):
        self.calculator = calculator
        self.backup_restore = backup_restore
        self.ledger_store = ledger_store
        self.currency_validator = currency_validator

    def add_transcation(self, currency, amount, tx_type):
        self.ledger_store.add_transaction(currency=currency, amount=amount, tx_type=tx_type)

    def get_balance(self, currency):
        currency_list = [c for c in self.ledger_store.ledgers.keys()]
        try:
            self.currency_validator.validate(currency=currency, currency_list=currency_list)
        except (TypeError, ValueError) as error_msg:
            return f"App Error:- {error_msg}"

        transactions = self.ledger_store.ledgers.get(currency.upper(), [])
        return self.calculator.calculate(transactions=transactions)

    def safe_transaction(self, currency, amount, tx_type, simulate_crash=False):
        snapshot = self.backup_restore.create_snapshot(ledgers=self.ledger_store.ledgers)
        try:
            self.ledger_store.add_transaction(currency=currency, amount=amount, tx_type=tx_type)
            if simulate_crash:
                raise RuntimeError("Simulated crash after write, before confirm")
        except Exception as error_msg:
            self.ledger_store.ledgers = self.backup_restore.restore(snapshot=snapshot)
            return f"Transaction Failed. Please try again later...."
        return f"Transaction Successfull"

class ReadOnlyWallet:
    def __init__(self, ledger_wallet):
        self.ledger_wallet = ledger_wallet

    def get_balance(self, currency):
        total_balance = self.ledger_wallet.get_balance(currency)
        return f"Your Current Balance is:- {total_balance}"
# ==================== RUNNING TESTS ====================

if __name__ == "__main__":
    wallet = LedgerWallet(
        calculator=BalanceCalculator(),
        backup_restore=BackupRestore(),
        ledger_store=LedgerStore(),
        currency_validator=CurrencyValidator()
    )

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

    # wallet.ledger_store.ledgers['USD'].append(Transaction(10, 'crdit', 'x'))  # typo test
    # print(f"Validation Catch:- {wallet.get_balance(currency='usd')}")   # expect raise error

    # print(wallet.get_balance(currency='usd'))   # normal case, expect same as pehle

    dashboard = ReadOnlyWallet(ledger_wallet=wallet)
    print(dashboard.get_balance(currency='usd'))
