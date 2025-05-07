# 📘 Use Case Functions (Markdown Summary)

---

## 👜 Asset Management

| Function                         | Description                                                   |
|----------------------------------|---------------------------------------------------------------|
| `createAsset(name, assetTypeId)` | Create a new asset (e.g. cash wallet or bank account).        |
| `getAllAssets()`                 | List all assets in the system.                                |
| `updateAsset(id, data)`         | Modify an asset’s name or type.                               |
| `deleteAsset(id)`               | Remove an asset (only if no related transactions).            |

---

## 🧾 Expense Management

| Function                                  | Description                                     |
|-------------------------------------------|-------------------------------------------------|
| `createExpense(description, expenseTypeId)` | Define a new expense item.                     |
| `getAllExpenses()`                        | List all defined expenses.                     |
| `updateExpense(id, data)`                | Update details of an existing expense.         |
| `deleteExpense(id)`                      | Delete an expense (if safe).                   |

---

## 💰 Transaction Management

| Function                                             | Description                                                           |
|------------------------------------------------------|-----------------------------------------------------------------------|
| `recordIncome(amount, assetId, contactId, date)`     | Record income to a selected asset, optionally from a contact.         |
| `recordPayment(amount, assetId, expenseId, contactId, date)` | Record a payment for an expense, optionally to a contact.       |
| `getTransactions()`                                  | Fetch all transactions (income + payments).                          |
| `getIncomeTransactions()`                            | Fetch only income transactions.                                      |
| `getPaymentTransactions()`                           | Fetch only payment transactions.                                     |
| `getTransactionsByMonth(month)`                      | Get all transactions in a given month.                               |

---

## 👥 Contact Management

| Function                                               | Description                                              |
|--------------------------------------------------------|----------------------------------------------------------|
| `createContact(name, businessName, phone, description, customerTypeId)` | Add a new contact (customer or vendor) with details.    |
| `getAllContacts()`                                     | List all saved contacts.                                 |
| `updateContact(id, data)`                              | Update contact info.                                     |
| `deleteContact(id)`                                    | Delete or deactivate a contact.                          |

---

## 🧾 Customer Type Management

| Function             | Description                                                   |
|----------------------|---------------------------------------------------------------|
| `getCustomerTypes()` | List available types (Customer, Vendor).                      |
| `createCustomer(...)`| Create a contact of type Customer (alternative to createContact). |
| `createVendor(...)`  | Create a contact of type Vendor.                              |

---

## 📊 Summary & Reports

| Function                  | Description                                                                      |
|---------------------------|----------------------------------------------------------------------------------|
| `getMonthlySummary(month)`| Show income and expense summary by asset type and expense type for the given month. |
