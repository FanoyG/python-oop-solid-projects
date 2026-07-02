# Project 1: The High-Throughput Vending Metrics Engine

## 📖 What is the Project?
The **High-Throughput Vending Metrics Engine** is a real-time analytics tracker designed to process and monitor physical inventory counts and financial transactions from thousands of isolated, automated vending machines. It acts as a central data collector that tracks exactly how much money each machine makes (`total_revenue`) and which items are being bought (`items_sold`).

---

## 🧠 What Did It Teach Me?
This project focuses heavily on backend data integrity, data protection, and clean object-oriented architecture. It teaches:

*   **The Single Responsibility Principle (SOLID):** The engine focus entirely on core business logic calculations rather than printing or formatting visual screens.
*   **Memory Isolation vs. Leaks:** How to correctly use standard instance variables (`self.payload`) so that data tracking for Machine A never accidentally leaks or overrides Machine B's data space.
*   **The Hidden Trap of External Mutation:** How easily external variables can corrupt internal records if data is not correctly encapsulated.

---

## 🛠️ How Did I Implement It?

### 1. Dynamic Data Buckets
Instead of creating empty keys manually, the pipeline reads metrics dynamically. If a machine reports data for the first time, it provisions a new tracking structure on-the-fly to guarantee zero crashes:
```python
if machine_id not in self.payload:
    self.payload[machine_id] = {"total_revenue": 0, "items_sold": {}}
```

### 2. The Deepcopy Encapsulation Shield
To protect internal records from being directly wiped or edited by external scripts, the `inventory_snapshot` property uses `copy.deepcopy()`. This hands out a clone of the data rather than a raw pointer to memory:
```python
@property
def inventory_snapshot(self):
    return copy.deepcopy(self.payload)
```

### 3. Strict Input Guardrails
Every record passes through severe type and boundary value validations (checking for invalid non-strings, negative numbers, or empty strings) before processing.

---

## 🏆 Outcome and Learning
By validating the architecture through a suite of robust **pytest** metrics, the code achieves several major engineering victories:

*   **Instance Independence:** Unit tests prove that modifying the datasets on Engine A keeps Engine B perfectly pure.
*   **Bulletproof Enforcer Shield:** Tests confirm that executing `.clear()` or altering a generated snapshot dictionary leaves the real database completely untouched.
*   **Parametrized Confidence:** Using parameterized loops validates multiple mathematical vectors seamlessly, handling correct calculations and flagging failure edge cases instantly.