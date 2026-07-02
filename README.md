# 🚀 Python OOP & SOLID: Project-by-Project

Mastering industry-standard backend design principles through real-world scenarios. Each project begins as a monolithic script and undergoes disciplined refactoring. Use the repository's commit history to track the step-by-step architectural evolution.

---

## 📂 Project Portfolio

### 🛠️ Project 1: High-Throughput Vending Metrics Engine
Real-time transaction and inventory telemetry processor for isolated automated vending machines.
*   **Status:** ![Done](https://shields.io)
*   **Key Focus:** Single Responsibility Principle (SRP), deep-copy memory isolation, strict data validation guardrails.
*   **Source:** [Explore Code Base](./project-1-vending-engine) | **Milestone Tag:** `p1-mvp`

### 💳 Project 2: Multi-Currency Ledger Wallet
Scalable double-entry ledger system handling isolated multi-currency transactions, balances, and filtering.
*   **Status:** ![In Progress](https://shields.io)
*   **Key Focus:** Interface Segregation, Open/Closed Principle, dynamic key-value ranking algorithms.
*   **Source:** [Explore Code Base](./project-2-ledger-wallet) | **Milestone Tags:** `p2-mvp`, `p2-srp`

---

## 🧠 Architectural Roadmap
1.  **The Monolith (MVP):** Getting raw functionality working quickly.
2.  **The Breakdown:** Splitting data mutation tasks away from output layouts.
3.  **The Shield:** Encapsulating state layers to deny direct external modifications.
4.  **The Test:** Validating strict instance isolation rules using `pytest`.
