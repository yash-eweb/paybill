# 90 % work
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

    # Create a settlement plan (dynamic approach)
    settlement_plan = []
    while any(balance != 0 for balance in balances.values()):
        debtors = [member for member, balance in balances.items() if balance < 0]
        creditors = [member for member, balance in balances.items() if balance > 0]

        for debtor in debtors:
            while balances[debtor] < 0:
                for creditor in creditors:
                    if balances[creditor] > 0:
                        amount = min(abs(balances[debtor]), balances[creditor])
                        settlement_plan.append({
                            'debtor': debtor,
                            'creditor': creditor,
                            'amount': amount
                        })
                        balances[debtor] += amount
                        balances[creditor] -= amount
                        break

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

# 70% work 
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

# try
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

    # Calculate initial debts correctly
    debts = defaultdict(lambda: defaultdict(int))
    for member in members:
        for expense in expenses:
            if member.user != expense.paid_by_user:
                debts[member.user][expense.paid_by_user] += per_member_share 

    # Create a directed graph to represent debts
    graph = DiGraph()
    for debtor, creditors in debts.items():
        for creditor, amount in creditors.items():
            graph.add_edge(debtor, creditor, weight=amount)

    # Find shortest paths (min-cost flow approximation)
    settlement_plan = []
    for debtor in debts:
        for creditor in debts[debtor]:
            try:
                path = shortest_path(graph, debtor, creditor, weight='weight')
                amount = debts[debtor][creditor]
                settlement_plan.append({
                    'debtor': path[0],
                    'creditor': path[-1],
                    'amount': amount,
                })
            except nx.NetworkXNoPath:
                pass  # No direct path, may be handled by other settlements

    # Optimize settlement plan (minimize transactions)
    optimized_plan = []
    while settlement_plan:
        settlement = settlement_plan.pop(0) 
        # Check if there's an offsetting transaction
        offsetting_settlement = next(
            (s for s in settlement_plan 
             if s['debtor'] == settlement['creditor'] and s['creditor'] == settlement['debtor']),
            None
        )
        if offsetting_settlement:
            # Offset transactions if possible
            settlement_plan.remove(offsetting_settlement) 
        else:
            optimized_plan.append(settlement)

    # Render the template
    return render(request, 'Group/group_detail.html', {
        'g': group,
        'members': members,
        'expenses': expenses,
        'balances': balances.items(),
        'settlement_plan': optimized_plan, 
        'per_member_share': per_member_share,
        'total_expense': total_expense,
    })


'''

#  it not work
'''
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group) 
    expenses = GroupExpense.objects.filter(group=group) 

    # Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount).quantize(Decimal('0.01')) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Track individual expenses per member
    individual_expenses = {member.user: Decimal(0) for member in members}
    for expense in expenses:
        if expense.is_shared:
            if expense.participating_members.count() > 0:
                num_participants = expense.participating_members.count()
                shared_amount = expense.amount / num_participants
                for member in expense.participating_members.all():
                    individual_expenses[member.user] -= shared_amount
            else:
                # Handle the case where no members participated (optional)
                # You could log a warning or take other actions
                print(f"Warning: Shared expense {expense.id} has no participating members.")

        else:
            individual_expenses[expense.paid_by_user] += expense.amount
    # Calculate balances 
    balances = {}
    for member in members:
        balances[member.user] = individual_expenses[member.user]

    # Create a settlement plan (dynamic approach)
    settlement_plan = []
    while any(balance != 0 for balance in balances.values()):
        debtors = [member for member, balance in balances.items() if balance < 0]
        creditors = [member for member, balance in balances.items() if balance > 0]

        for debtor in debtors:
            while balances[debtor] < 0:
                for creditor in creditors:
                    if balances[creditor] > 0:
                        amount = min(abs(balances[debtor]), balances[creditor])
                        settlement_plan.append({
                            'debtor': debtor,
                            'creditor': creditor,
                            'amount': amount
                        })
                        balances[debtor] += amount
                        balances[creditor] -= amount
                        break

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


#  combine result
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

    # Create a graph for MST-based settlement
    G = nx.Graph()
    for user1, balance1 in balances.items():
        for user2, balance2 in balances.items():
            if user1 != user2 and balance1 * balance2 < 0:  # Create edges between debtors and creditors
                G.add_edge(user1, user2, weight=-balance1)  # Weight is the debt to be settled

    try:
        mst = nx.minimum_spanning_tree(G)
        # Generate settlement messages based on the MST
        settlement_plan = []
        for (user1, user2) in mst.edges():
            amount_to_settle = abs(G[user1][user2]['weight'])
            settlement_plan.append({
                'debtor': user1,
                'creditor': user2,
                'amount': amount_to_settle
            })
    except nx.NetworkXNoPath:
        # Handle cases where no MST can be found (e.g., circular debts)
        # Fallback to dynamic settlement
        settlement_plan = []
        positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
        negative_balances = {user: balance for user, balance in balances.items() if balance < 0}

        while positive_balances and negative_balances:
            for pos_user, pos_balance in list(positive_balances.items()):
                for neg_user, neg_balance in list(negative_balances.items()):
                    if pos_balance == 0 or neg_balance == 0:
                        continue

                    # Settle the balance by transferring the smallest amount
                    amount_to_settle = min(pos_balance, -neg_balance)

                    # Record the settlement message
                    settlement_plan.append({
                        'debtor': neg_user,
                        'creditor': pos_user,
                        'amount': amount_to_settle
                    })

                    # Update the balances after settling
                    positive_balances[pos_user] -= amount_to_settle
                    negative_balances[neg_user] += amount_to_settle

                    # Remove fully settled balances
                    if positive_balances[pos_user] == 0:
                        del positive_balances[pos_user]
                    if negative_balances[neg_user] == 0:
                        del negative_balances[neg_user]

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