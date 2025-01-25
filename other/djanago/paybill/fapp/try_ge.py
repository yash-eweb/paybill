def calculate_balances(members, expenses):
  """
  Calculates the balances for each member in a group expense.

  Args:
    members: A list of member names.
    expenses: A dictionary where keys are expense names and values are tuples 
              containing the total expense amount and the name of the payer.

  Returns:
    A dictionary where keys are member names and values are the amount 
    that member needs to pay or receive.
  """

  balances = {member: 0 for member in members}
  total_expense = sum(expense[0] for expense in expenses.values())
  per_member_share = total_expense / len(members)

  for member in members:
    for expense_name, (amount, payer) in expenses.items():
      if payer == member:
        balances[member] -= amount
      else:
        balances[member] += amount / len(members)

  for member in members:
    balances[member] = round(balances[member], 2)

  return balances

# Get input dynamically
members = input("Enter members separated by commas: ").split(',')
num_expenses = int(input("Enter the number of expenses: "))

expenses = {}
for i in range(num_expenses):
  expense_name = input(f"Enter expense name {i+1}: ")
  expense_amount = float(input(f"Enter expense amount for {expense_name}: "))
  payer = input(f"Enter payer for {expense_name}: ")
  expenses[expense_name] = (expense_amount, payer)

# Calculate balances
balances = calculate_balances(members, expenses)

# Output the balances
for member, balance in balances.items():
  if balance > 0:
    print(f"{member} needs to pay ₹{balance:.2f} to q") 
  elif balance < 0:
    print(f"cv needs to pay ₹{-balance:.2f} to {member}")