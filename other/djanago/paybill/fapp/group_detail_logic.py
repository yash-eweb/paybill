# https://gemini.google.com/app/d0c9715c0c3c3d7e?hl=en-IN


'''@login_required
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.all()
    expenses = GroupExpense.objects.filter(group=group)
    balances = GroupBalance.objects.filter(group=group)

    # Check if the current user is the creator/admin of the group
    is_admin = group.created_by == request.user

    # Calculate the total expense
    total_expense = sum(expense.amount for expense in expenses)
    share_per_person = Decimal(total_expense) / Decimal(len(members)) if members else Decimal(0)

    # Check if the user is a member of the group
    is_member = GroupMember.objects.filter(group=group, user=request.user).exists()
    
    if not is_member:
        return HttpResponseForbidden("You are not a member of this group.")


    # Calculate each member's balance
    balances = []
    for member in members:
        paid_by_member = sum(expense.amount for expense in expenses if expense.paid_by_user == member)
        balance = Decimal(paid_by_member) - share_per_person
        balances.append({'user': member, 'balance': balance})

    # Separate payers (owe money) and receivers (are owed money)
    payers = [b for b in balances if b['balance'] < 0]
    receivers = [b for b in balances if b['balance'] > 0]

    # Create transactions to settle balances
    transactions = []

    for payer in payers:
        while payer['balance'] < 0 and receivers:
            receiver = receivers[0]
            amount_to_pay = min(abs(payer['balance']), receiver['balance'])

            transactions.append({
                'from': payer['user'].username,
                'to': receiver['user'].username,
                'amount': round(amount_to_pay, 2),
            })

            # Update balances
            payer['balance'] += amount_to_pay
            receiver['balance'] -= amount_to_pay

            # Remove settled receivers
            if receiver['balance'] == 0:
                receivers.pop(0)
    context = {
        'g': group,
        'members': members,
        'expenses': expenses,
        'transactions': transactions,  # Pass the transactions to the template
        'is_admin': is_admin,  # Pass whether the user is admin or not
        'balances': balances
    }
    return render(request, 'Group/group_detail.html', context)'''



# a needs to pay ₹130 to the group   only kone ketla baki che te na mate
'''def group_detail(request, id):
    # group_details_dm(request, id)
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Step 1: Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Step 2: Track payments by each member (Dynamic payment tracking)
    payments = {member.user: Decimal(0) for member in members}

    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

   
    # Step 4: Recalculate balances (who owes what)
    balances = {}
    for member in members:
        balance = payments[member.user] - per_member_share
        balances[member.user] = balance

    balance_messages = []

# Check balances for each member and generate messages
    for user, balance in balances.items():
        if balance < 0:  # Negative balance means the user owes money
            amount_owed = abs(balance)
            balance_messages.append(f"{user} needs to pay ₹{amount_owed:.2f} to the group")

    return render(request, 'Group/group_detail.html', {
        'g': group,
        'members': members,
        'expenses': expenses,
        'balance_messages': balance_messages,
        'per_member_share': int(per_member_share),
        'total_expense':total_expense,
    })'''


# 3 jan 25 
'''
def group_detail(request, id):
    # group_details_dm(request, id)
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Step 1: Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Step 2: Track payments by each member (Dynamic payment tracking)
    payments = {member.user: Decimal(0) for member in members}

    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

    # Step 3: Adjust payments dynamically (e.g., additional payments made by users like 'a' for tea)
    # You can dynamically update the payments here based on user actions
    # For example:
    # user_specific_payments = {
    #     'a': Decimal(30),  # Example: a paid ₹30 for tea
    # }
    
    # for user, amount in user_specific_payments.items():
    #     if user in payments:
    #         payments[user] += amount  # Add any additional payment to the user's total payment

    # Step 4: Recalculate balances (who owes what)
    balances = {}
    for member in members:
        balance = payments[member.user] - per_member_share
        balances[member.user] = balance

    # Step 5: Separate positive and negative balances (who needs to pay whom)
    positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
    negative_balances = {user: balance for user, balance in balances.items() if balance < 0}

    # Step 6: Generate dynamic settlement logic
    balance_messages = []

    # Make copies of positive_balances and negative_balances for iteration
    positive_balances_copy = positive_balances.copy()
    negative_balances_copy = negative_balances.copy()

    # Settle the balances dynamically between positive and negative balances
    for pos_user, pos_balance in positive_balances_copy.items():
        for neg_user, neg_balance in negative_balances_copy.items():
            if pos_balance == 0 or neg_balance == 0:
                continue

            # Calculate the settlement amount (the minimum of positive and negative balances)
            amount_to_settle = min(abs(pos_balance), abs(neg_balance))

            # Record the settlement message dynamically
            balance_messages.append(
                f"{neg_user} needs to pay ₹{amount_to_settle:.2f} to {pos_user}"
            )

            # Update the balances after settling
            positive_balances[pos_user] -= amount_to_settle
            negative_balances[neg_user] += amount_to_settle

            # Remove fully settled balances
            if positive_balances[pos_user] == 0:
                del positive_balances[pos_user]
            if negative_balances[neg_user] == 0:
                del negative_balances[neg_user]
    for message in balance_messages:
        print(message)

    # Step 7: Render the result dynamically with real-time data
    return render(request, 'Group/group_detail.html', {
        'g': group,
        'members': members,
        'expenses': expenses,
        'balance_messages': balance_messages,
        'per_member_share': per_member_share,
        'total_expense':total_expense,
    })



'''


'''
@login_required
def calculate_balances(expenses, members):
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = len(members)
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Track how much each user has paid
    paid_amounts = {}
    for member in members:
        user = member.user  # Access the user from GroupMember
        paid_amounts[user] = sum(Decimal(expense.amount) for expense in expenses if expense.paid_by_user == user)
    
    # Calculate balances for each member
    balances = {}
    for member in members:
        user = member.user  # Access the user from GroupMember
        paid_amount = paid_amounts.get(user, Decimal(0))
        balances[user] = paid_amount - per_member_share

    return balances, per_member_share



def settle_balances(balances):
    """
    Dynamically settle balances among members and generate the correct transactions.
    """
    transactions = []
    creditors = []  # People who are owed money
    debtors = []    # People who owe money

    # Separate creditors and debtors
    for member, balance in balances.items():
        if balance > 0:  # Member should receive money
            creditors.append([member, balance])  # Use mutable lists for updates
        elif balance < 0:  # Member owes money
            debtors.append([member, -balance])  # Store as positive for easier calculations

    # Iteratively settle balances
    while creditors and debtors:
        # Take the first creditor and debtor
        creditor, credit_amount = creditors[0]
        debtor, debt_amount = debtors[0]

        # Determine the amount to settle (minimum of what's owed and to be received)
        settlement_amount = min(credit_amount, debt_amount)

        # Add the transaction to the list
        transactions.append(f"{debtor.username} needs to pay ₹{settlement_amount:.2f} to {creditor.username}")

        # Adjust balances
        creditors[0][1] -= settlement_amount
        debtors[0][1] -= settlement_amount

        # Remove settled creditor or debtor
        if creditors[0][1] == 0:
            creditors.pop(0)  # Remove the creditor if fully settled
        if debtors[0][1] == 0:
            debtors.pop(0)  # Remove the debtor if fully settled

    return transactions

'''


'''
# @login_required
# def group_detail(request, id):
#     group = get_object_or_404(Group, id=id)

#     # Check if the user is a member of the group
#     is_member = GroupMember.objects.filter(group=group, user=request.user).exists()
#     if not is_member:
#         # return redirect('allgroup')
#         return HttpResponseForbidden("You are not a member of this group.")

#     # Group details
#     members = GroupMember.objects.filter(group=group)
#     expenses = GroupExpense.objects.filter(group=group)

#     '''# Calculate total expense and per-member share

#     # total_expense = sum(expense.amount for expense in expenses)
#     # num_members = members.count()
#     # share_per_member = total_expense / num_members if num_members > 0 else 0'''

#     total_expense = sum(Decimal(expense.amount) for expense in expenses)  # Use Decimal for currency
#     num_members = members.count()
#     # print(f"No OF member :- \t {num_members}")
#     share_per_member = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

#     # Calculate balances for each member
#     balances = {}
#     for member in members:
#         paid_amount = sum(expense.amount for expense in expenses if expense.paid_by_user == member.user)
#         balances[member.user] = paid_amount - share_per_member

#         '''
#         paid_amount = 0
#         for expense in expenses:
#             if expense.paid_by_user == member.user:
#                 paid_amount += expense.amount
#         '''

#     # Prepare balance messages
#     balance_messages = []
#     positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
#     negative_balances = {user: balance for user, balance in balances.items() if balance < 0}

#     '''
#     # Initialize two empty dictionaries to store users with positive and negative balances
#         positive_balances = {}
#         negative_balances = {}

#     # Iterate over each user and their balance in the balances dictionary
#     for user, balance in balances.items():
#         if balance > 0:
#             positive_balances[user] = balance  # Add users with a positive balance to positive_balances
#         elif balance < 0:
#             negative_balances[user] = balance  # Add users with a negative balance to negative_balances

#     '''

#     for pos_user, pos_balance in positive_balances.items():
#         for neg_user, neg_balance in list(negative_balances.items()):
#             if pos_balance == 0 or neg_balance == 0:
#                 continue

#             amount_to_settle = min(pos_balance, -neg_balance)

#             balance_messages.append(
#                 f"{neg_user.username} needs to pay ₹{amount_to_settle:.2f} to {pos_user.username}"
#             )

#             # Update balances for next iteration
#             positive_balances[pos_user] -= amount_to_settle
#             negative_balances[neg_user] += amount_to_settle

#             # Remove fully settled balances
#             if positive_balances[pos_user] == 0:
#                 break
#             if negative_balances[neg_user] == 0:
#                 del negative_balances[neg_user]

#     return render(request, 'Group/group_detail.html', {
#         'g': group,
#         'members': members,
#         'expenses': expenses,
#         'balances': balances.items(),
#         'balance_messages': balance_messages,
#     })



# kish ko kit na dena he vo 
'''
import pymysql  # or your preferred library for database connection

# Database connection
connection = pymysql.connect(
    host="localhost",        # Change to your database host
    user="root",             # Your database username
    password="password",     # Your database password
    database="your_database" # Your database name
)

try:
    # Fetch balances from the database
    with connection.cursor() as cursor:
        # Query to fetch all users and their balances
        cursor.execute("SELECT username, balance FROM balances")
        result = cursor.fetchall()

    # Initialize balances
    negative_balances = {}
    positive_balances = {}

    # Process database results
    for row in result:
        username = row[0]
        balance = row[1]
        if balance < 0:
            negative_balances[username] = abs(balance)  # Make negative balances positive for calculation
        elif balance > 0:
            positive_balances[username] = balance

    # Settlement Logic
    balance_messages = []

    while negative_balances:
        for neg_user, neg_balance in list(negative_balances.items()):
            if neg_balance == 0:
                continue  # Skip if the negative balance is settled

            # Iterate over users with positive balances
            for pos_user, pos_balance in list(positive_balances.items()):
                if pos_balance == 0:
                    continue  # Skip if the positive balance is already settled

                # Calculate the amount to settle between the two users
                amount_to_settle = min(neg_balance, pos_balance)

                # Add settlement message
                balance_messages.append(
                    f"{neg_user} needs to pay ₹{amount_to_settle:.2f} to {pos_user}"
                )

                # Update the balances
                negative_balances[neg_user] -= amount_to_settle
                positive_balances[pos_user] -= amount_to_settle

                # Remove fully settled balances
                if positive_balances[pos_user] == 0:
                    del positive_balances[pos_user]
                if negative_balances[neg_user] == 0:
                    del negative_balances[neg_user]

                # Stop when there is no more negative balance
                if not negative_balances:
                    break

    # Print settlement messages
    for message in balance_messages:
        print(message)

finally:
    connection.close()



'''


# a need to pay 140 to er after, a  pay 30 for tea
'''
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Step 1: Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Step 2: Track payments by each member
    payments = {member.user: Decimal(0) for member in members}

    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

    # Step 3: Calculate balance (how much each member owes or is owed)
    balances = {}
    for member in members:
        balance = payments[member.user] - per_member_share
        balances[member.user] = balance

    # Step 4: Prepare the settlement logic for balances (who owes whom)
    balance_messages = []
    
    # Separate positive and negative balances
    positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
    negative_balances = {user: balance for user, balance in balances.items() if balance < 0}

    # Debugging: Check before settlement
    print("Positive Balances:", positive_balances)
    print("Negative Balances:", negative_balances)

    # Step 5: Settle the balances dynamically
    for pos_user, pos_balance in list(positive_balances.items()):
        for neg_user, neg_balance in list(negative_balances.items()):
            if pos_balance == 0 or neg_balance == 0:
                continue

            # Settle the balance by transferring the smallest amount of the positive and negative balances
            amount_to_settle = min(pos_balance, -neg_balance)
            
            # Record the settlement message
            balance_messages.append(
                f"{neg_user.username} needs to pay ₹{amount_to_settle:.2f} to {pos_user.username}"
            )

            # Update the balances after settling
            positive_balances[pos_user] -= amount_to_settle
            negative_balances[neg_user] += amount_to_settle

            # Remove fully settled balances
            if positive_balances[pos_user] == 0:
                del positive_balances[pos_user]
            if negative_balances[neg_user] == 0:
                del negative_balances[neg_user]

    # Debugging: Final settlement checks
    print("Positive Balances After Settlement:", positive_balances)
    print("Negative Balances After Settlement:", negative_balances)

    # Step 6: Render the page with the group and balance data
    return render(request, 'Group/group_detail.html', {
        'g': group,
        'members': members,
        'expenses': expenses,
        'balances': balances.items(),
        'balance_messages': balance_messages,
        'per_member_share': per_member_share,
    })

'''

#  new  logic code 
'''
def group_detail(request, id):
    # Step 1: Get group and related data
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Step 2: Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Step 3: Track payments by each member
    payments = {member.user: Decimal(0) for member in members}
    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

    # Step 4: Calculate balances
    balances = {}
    for member in members:
        balance = payments[member.user] - per_member_share
        balances[member.user] = balance

    # Step 5: Separate positive and negative balances
    positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
    negative_balances = {user: balance for user, balance in balances.items() if balance < 0}

    # Debugging: Print initial balances
    print("Initial Positive Balances:", positive_balances)
    print("Initial Negative Balances:", negative_balances)

    # Step 6: Settle balances
    # Step 6: Settle the balances dynamically
    balance_messages = []
    while negative_balances:
        for neg_user, neg_balance in list(negative_balances.items()):
            if neg_balance == 0:
                continue
            
            # Find the user who is owed the most (positive balance)
            for pos_user, pos_balance in list(positive_balances.items()):
                if pos_balance == 0:
                    continue

                # Calculate how much cv needs to pay
                amount_to_settle = min(abs(neg_balance), pos_balance)

                # Add the settlement message
                balance_messages.append(
                    f"{neg_user.username} needs to pay ₹{amount_to_settle:.2f} to {pos_user.username}"
                )

                # Update the balances after settling
                negative_balances[neg_user] -= amount_to_settle
                positive_balances[pos_user] -= amount_to_settle

                # Remove fully settled balances
                if positive_balances[pos_user] == 0:
                    del positive_balances[pos_user]
                if negative_balances[neg_user] == 0:
                    del negative_balances[neg_user]

                # After each settlement, track the remaining balance for each user
                print(f"Remaining Balance for {neg_user.username}: ₹{negative_balances.get(neg_user, 0):.2f}")
                print(f"Remaining Balance for {pos_user.username}: ₹{positive_balances.get(pos_user, 0):.2f}")

                # Stop when there is no more negative balance
                if not negative_balances:
                    break

# Print settlement messages
    for message in balance_messages:
        print(message)

# Debugging: Final settlement checks
    print("Positive Balances After Settlement:", positive_balances)
    print("Negative Balances After Settlement:", negative_balances)
    print("Settlement Messages:", balance_messages)

'''


#  a need to paid 30rs to er 
'''
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Step 1: Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Step 2: Track payments by each member
    payments = {member.user: Decimal(0) for member in members}

    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

    # Step 3: Calculate balance (how much each member owes or is owed)
    balances = {}
    for member in members:
        balance = payments[member.user] - per_member_share
        balances[member.user] = balance

    # Step 4: Prepare the settlement logic for balances (who owes whom)
    balance_messages = []
    positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
    negative_balances = {user: balance for user, balance in balances.items() if balance < 0}

    # Step 5: Settle the balances
    for pos_user, pos_balance in list(positive_balances.items()):
        for neg_user, neg_balance in list(negative_balances.items()):
            if pos_balance == 0 or neg_balance == 0:
                continue

            # Settle the balance by transferring the smallest amount of the positive and negative balances
            amount_to_settle = min(pos_balance, -neg_balance)
            balance_messages.append(
                f"{neg_user.username} needs to pay ₹{amount_to_settle:.2f} to {pos_user.username}"
            )

            # Update the balances after settling
            positive_balances[pos_user] -= amount_to_settle
            negative_balances[neg_user] += amount_to_settle

            # Remove fully settled balances
            if positive_balances[pos_user] == 0:
                del positive_balances[pos_user]
            if negative_balances[neg_user] == 0:
                del negative_balances[neg_user]

    # Step 6: Render the page with the group and balance data
    return render(request, 'Group/group_detail.html', {
        'g': group,
        'members': members,
        'expenses': expenses,
        'balances': balances.items(),
        'balance_messages': balance_messages,
        'per_member_share': per_member_share,
    })

'''


# last code
'''
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Track payments by each member
    payments = {member.user: Decimal(0) for member in members}
    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

    # Calculate balances (how much each member owes or is owed)
    balances = {}
    for member in members:
        balances[member.user] = payments[member.user] - per_member_share

    # Create a settlement plan (simplified for this specific scenario)
    settlement_plan = []
    for member in members:
        if member.user != expense.paid_by_user and balances[member.user] < 0: 
            settlement_plan.append({
                'debtor': member.user,
                'creditor': expense.paid_by_user,
                'amount': abs(balances[member.user])
            })

    # Render the template with the settlement plan

    return render(request, 'Group/group_detail.html', {
        
        'g': group,
        'members': members,
        'expenses': expenses,
        'balances': balances.items(),
        'settlement_plan': settlement_plan,
        'per_member_share': per_member_share,
        'total_expense': total_expense,
    })


'''

'''
def add_group_expense(request, id):
    if request.method == "POST":
        # amount = float(request.POST['amount'])
        amount = Decimal(request.POST['amount'])  # Use Decimal instead of float
        # amount = Decimal(request.POST.get('amount'))  # Convert from string/float to Decimal
        category = request.POST['category']
        paid_by_user_id = request.POST['paid_by_user']
        description = request.POST['description']
        date = request.POST['date']

        group = Group.objects.get(id=id)
        paid_by_user = User.objects.get(id=paid_by_user_id)
        members = GroupMember.objects.filter(group=group)

        # Add expense to GroupExpense
        GroupExpense.objects.create(
            group=group, 
            amount=amount, 
            category=category, 
            paid_by_user=paid_by_user, 
            description=description, 
            date=date
        )

        # Calculate balances
        per_person_share = Decimal(amount) / Decimal(len(members))
        for member in members:
            balance_entry, created = GroupBalance.objects.get_or_create(group=group, user=member.user)

            # Ensure balance is explicitly converted to Decimal
            balance_entry.balance = Decimal(balance_entry.balance)  # If not already a Decimal


            if member.user == paid_by_user:
                balance_entry.balance += Decimal(amount) - Decimal(per_person_share)  # Explicitly convert to Decimal
            else:
                balance_entry.balance -= per_person_share  # Explicitly convert to Decimal
            
            balance_entry.save()

        return redirect('group_detail', id=id)
        

    group = Group.objects.get(id=id)
    members = GroupMember.objects.filter(group=group)
    return render(request, 'Group/add_group_expense.html', {'group': group, 'members': members})


'''