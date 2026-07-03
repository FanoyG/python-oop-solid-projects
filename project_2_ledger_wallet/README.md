# 📘 Project 2 Summary: SOLID Ledger Wallet Prototype

This document captures the structural design changes made to our multi-currency wallet. The goal of this phase was to pivot from a single messy script into a modular, clean **SOLID-compliant prototype** featuring basic crash-safe state management.

---

## 🚀 The Core Product (MVP)
The application acts as a lightweight, memory-based digital transaction log. It tracks financial records across multiple currencies with localized fault tolerance.

### 1. The Core Transaction Structure
Every transaction is modeled cleanly as its own individual data object containing an amount, a transaction direction rule (`credit`/`debit`), and an automated UTC tracking timestamp.

```python
class Transaction:
    def __init__(self, amount, tx_type, timestamp):
        self.amount = amount
        self.type = tx_type
        self.timestamp = timestamp
```

### 2. The Disaster Recovery System (Crash-Safe Rollbacks)
* **The Analogy:** Think of this like hitting `Ctrl + S` in a video game right before a difficult boss fight. If your character dies (the system crashes), you don't lose your whole game save; you simply reload the last safe checkpoint.

* **The Code:** The `safe_transaction` method creates an in-memory snapshot before attempting to append new data. If a runtime failure triggers, the ledger state instantly rolls back to its pre-transaction state.

```python
    def safe_transaction(self, currency, amount, tx_type, simulate_crash=False):
        # 1. Create a safe restore point
        snapshot = self.backup_restore.create_snapshot(ledgers=self.ledger_store.ledgers)
        try:
            self.ledger_store.add_transaction(currency=currency, amount=amount, tx_type=tx_type)
            if simulate_crash:
                raise RuntimeError("Simulated crash after write, before confirm")
        except Exception as error_msg:
            # 2. Crash intercepted! Rolling back instantly.
            self.ledger_store.ledgers = self.backup_restore.restore(snapshot=snapshot)
            return f"Transaction Failed. Please try again later...."
        return f"Transaction Successfull"
```

---

## 💻 Local Setup & Version Control

To copy this repository and explore the codebase on your local computer, run these commands in your terminal:

```bash
# 1. Clone the repository to your local machine
git clone https://github.com/FanoyG/python-oop-solid-projects.git

# 2. Move inside the project directory
cd python-oop-solid-projects
```

### 📍 Git Release Checkpoints
You can navigate different stages of this project's evolutionary codebase using these git tags:
* **`p2-mvp`** — The initial working multi-currency wallet before applying SOLID principles.
* **`p2-solid-complete`** — The finalized, refactored prototype with clean SRP, OCP, ISP, and DIP architectures.

To hop to a specific architectural phase locally, use:
```bash
git checkout <tag_name>
```
---
## 🛠️ The SOLID Upgrades

### 👯 1. Transaction Duplicate Detection (`__eq__` Override)
* **The Analogy:** Imagine a bouncer at a club door holding a clipboard. If two people show up with the exact same Name, Age, and ID, the bouncer knows it is a duplicate ticket scam and blocks the second person.

* **The Code:** We customized Python's internal logic operator (`__eq__`) so the system can natively spot when two different object instances contain identical financial data.

```python
    def __eq__(self, other):
        return (
            self.amount == other.amount and
            self.type == other.type and
            self.timestamp == other.timestamp
        )
```

---

### 🧱 2. Single Responsibility Principle (SRP)
* **The Analogy:** A restaurant where a single person cooks, waiter-hosts, cleans dishes, manages accounting, and sweeps floors will eventually burn down. You need dedicated workers for dedicated jobs
.
* **The Code:** We decoupled the core codebase. Instead of one massive class doing everything, we split it into **5 highly focused, specialized structural classes**:

* **`class Transaction`**: 📝 Defines what a transaction data container looks like.
* **`class LedgerStore`**: 🗄️ Physically saves, initializes, and appends logs.
* **`class BalanceCalculator`**: 🧮 Computes pure mathematical balance summations.
* **`class BackupRestore`**: 💾 Creates and loads deeply isolated system snapshots.
* **`class CurrencyValidator`**: 🔍 Verifies data safety checks on currency type inputs.

---

### 🔌 3. Open/Closed Principle (OCP)
* **The Analogy:** Your wall outlet is *closed* for structural modifications (you don't tear down the drywall to run a laptop), but it is *open* to extension (you can plug in a phone, lamp, or vacuum cleaner plug interchangeably).

* **The Code:** We threw away long, messy, hard-coded `if tx_type == "credit": else if...` logical loops. Instead, we mapped routing behavior using an extensible `TYPE_RULE` dictionary combined with clean lookup calls.

```python
class BalanceCalculator:
    positive = lambda amount: amount
    negative = lambda amount: -amount

    # Extensible configuration map! 
    TYPE_RULE = {
        "credit" : positive,
        'debit'  : negative
    }
    
    def calculate(self, transactions):
        total = 0
        for transaction in transactions:
            rule = self.TYPE_RULE.get(transaction.type)
            # Safe checking logic remains completely untouched!
            ...
            total += rule(transaction.amount)
        return total
```

---

### 🧬 4. Liskov Substitution Principle (LSP) — *Honest Design Caveat*
* **The Concept:** If it looks like a duck and quacks like a duck, but needs batteries to run, your inheritance hierarchy is broken. Subclasses must be able to replace their parents cleanly.

* **Our Project Reality:** **LSP is satisfied purely by the elimination of risk.** Because we chose a strict **composition-based architecture** and used no inheritance (`class SubClass(ParentClass)`) anywhere in Project 2, it is impossible to violate LSP. 

* *Interview Note:* LSP is not actively demonstrated or tested in this specific project codebase due to the total absence of subclasses. Real demonstration of subtype substitution will be introduced in later iterations (Project 5).

---

### 🛡️ 5. Interface Segregation Principle (ISP)
* **The Analogy:** You wouldn't give a valet parking attendant your entire keyring containing your home deadbolts, office keycards, and safe deposit keys. You hand them the valet key that only turns on the car engine.

* **The Code:** We isolated administrative features by building a secure interface layer wrapper called `ReadOnlyWallet`. Clients who only need access for basic metrics or display dashboards are restricted to this wrapper, hiding all dangerous structural modifying functions (like `add_transaction` or `safe_transaction`).

```python
class ReadOnlyWallet:
    def __init__(self, ledger_wallet):
        self.ledger_wallet = ledger_wallet

    # Only balance lookup is exposed to this client type!
    def get_balance(self, currency):
        total_balance = self.ledger_wallet.get_balance(currency)
        return f"Your Current Balance is:- {total_balance}"
```

---

### 🏗️ 6. Dependency Inversion Principle (DIP)
* **The Analogy:** A ceiling lamp shouldn't be permanently soldered straight into the electrical wires inside your roof. It should plug into a standard socket. That way, you can replace a burnt bulb or swap out the whole light fixture without calling an electrician to re-wire your building.

* **The Code:** `LedgerWallet` no longer creates its own database or validation objects inside its constructor using hardcoded imports. Instead, it accepts its engines via **Constructor Injection**. 

```python
class LedgerWallet:
    # All dependency engines are plugged in externally!
    def __init__(self, calculator, backup_restore, ledger_store, currency_validator):
        self.calculator = calculator
        self.backup_restore = backup_restore
        self.ledger_store = ledger_store
        self.currency_validator = currency_validator
```
* **Real-World Benefit:** This design makes the system highly testable. For example, during automated tests, we can instantly swap out the real `BalanceCalculator` and plug in a fake "mock" calculator to test how the wallet reacts without running the actual math engine.

---

### 🪲 Technical Note: Internal Method Typo
Please note that in the initial prototype implementation, the execution method in `LedgerWallet` contains a typo: named **`add_transcation`** (missing the 'a'). To maintain execution parity across downstream systems without breaking the script runtime, the README references it exactly as written until the next planned code refactor sweep.

---

## ⚠️ Known Limitations & Roadmap (What's Next)
This project is an architectural prototype for validating SOLID patterns; it is **not** enterprise production software. The current limitations and future scope include:

### 🔥 1. Zero Concurrency Handling (System-Thinking Depth)
* **The Bottleneck:** The current prototype has absolutely no awareness of simultaneous actions. If two users try to withdraw or transfer money at the exact same fraction of a second, the system will face data conflicts and corrupt the financial balances. 
* *Next Step:* Implement file/database locking mechanisms or sequential processing queues to ensure transactions process safely one-by-one.

### 2. In-Memory Storage & Performance Constraints
* **The Bottleneck:** Financial data is preserved purely in temporary computer memory (`self.ledgers = {}`). If you turn off the script, all data vanishes. Furthermore, the rollback mechanism utilizes a heavy Python `deepcopy` snapshot, which will slow down drastically as more transactions are added.
* *Next Step:* Introduce a hard-drive tracking log or plug in a permanent database engine (like SQL).

### 3. Manual OCP Extensions
* **The Bottleneck:** While the `TYPE_RULE` map removes messy `if/elif` statements, adding a brand new transaction type still requires a developer to open this code file and manually type it into the class dictionary.
* *Next Step:* Establish a system where new rules can be loaded dynamically from a separate configuration file without touching the code.

### 4. Testing Deficit
* **The Bottleneck:** The code is currently verified using manual print statements at the bottom of the script rather than a standard testing framework.
