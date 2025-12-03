from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from decimal import Decimal, InvalidOperation
import logging
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum
import json

@login_required
def home(request):
    form = TransactionForm(data=request.POST or None)
    if request.method == 'POST':
        pk = request.POST['account']
        # Redirect instead of calling the view directly
        if pk == '17':
            return redirect('balance2', pk=pk)
        else:
            return redirect('balance', pk=pk)
    content = {'form': form}
    return render(request, 'checkbook/index.html', content)


@login_required
def create_account(request):
    form = AccountForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')
    content = {'form': form}
    return render(request, 'checkbook/CreateNewAccount.html', content)


@login_required
def balance_sheet(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    # Get all transactions ordered by date (oldest first for correct balance calculation)
    all_transactions = list(Transaction.Transactions.filter(account=pk).select_related('account').order_by('date'))
    
    # Calculate running balance for ALL transactions
    current_total = account.initial_deposit
    transactions_with_balance = []
    
    for t in all_transactions:
        try:
            amount = t.amount
            
            if t.type == 'Deposit':
                current_total += amount
            else:
                current_total -= amount
            
            transactions_with_balance.append((t, current_total))
                
        except (ValueError, TypeError, InvalidOperation) as e:
            logging.error(f"Error processing transaction {t.id}: {str(e)}")
            continue
    
    # Reverse to show newest first
    transactions_with_balance.reverse()
    
    # Pagination on the pre-calculated list
    paginator = Paginator(transactions_with_balance, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Convert page items to dictionary for template
    table_contents = {transaction: balance for transaction, balance in page_obj}
    # Pass a list of (transaction, balance) tuples to the template
    table_contents = list(page_obj)
    
    content = {
        'account': account,
        'table_contents': table_contents,
        'balance': current_total,
        'page_obj': page_obj
    }
    return render(request, 'checkbook/BalanceSheet.html', content)

@login_required
def balance2(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    # Get all transactions ordered by date (oldest first for correct balance calculation)
    all_transactions = list(Transaction.Transactions.filter(account=pk).select_related('account').order_by('date'))
    
    # Calculate running balance for ALL transactions
    current_total = account.initial_deposit
    transactions_with_balance = []
    
    for t in all_transactions:
        try:
            amount = t.amount
            
            if t.type == 'Deposit':
                current_total += amount
            else:
                current_total -= amount
            
            transactions_with_balance.append((t, current_total))
                
        except (ValueError, TypeError, InvalidOperation) as e:
            logging.error(f"Error processing transaction {t.id}: {str(e)}")
            continue
    
    # Reverse to show newest first
    transactions_with_balance.reverse()
    
    # Pagination on the pre-calculated list
    paginator = Paginator(transactions_with_balance, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Convert page items to dictionary for template
    table_contents = {transaction: balance for transaction, balance in page_obj}
   # Pass a list of (transaction, balance) tuples to the template
    table_contents = list(page_obj)
    
    content = {
        'account': account,
        'table_contents': table_contents,
        'balance': current_total,
        'page_obj': page_obj
    }
    return render(request, 'checkbook/BalanceSheet2.html', content)

@login_required
def add_transaction(request, account_pk):
    account = get_object_or_404(Account, pk=account_pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.account = account
            tx.save()
            # Redirect to euro view for account 2, otherwise regular balance
            if str(account.pk) == '2':
                return redirect('balance2', pk=account.pk)
            return redirect('balance', pk=account.pk)
    else:
        form = TransactionForm(initial={'account': account})
    return render(request, 'checkbook/AddTransaction.html', {'form': form, 'account': account})

@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction.Transactions.select_related('account'), pk=pk)
    account = transaction.account  # Always get the related account
    form = TransactionForm(data=request.POST or None, instance=transaction)
    if request.method == 'POST':
        if form.is_valid():
            updated = form.save()
            account_pk = getattr(updated, 'account_id', None) or (updated.account.pk if getattr(updated, 'account', None) else None)
            if str(account_pk) == '2':
                return redirect('balance2', pk=account_pk)
            return redirect('balance', pk=account_pk)
    else:
        form = TransactionForm(instance=transaction)
        print(f"Form date field value: {form['date'].value()}")
        print(f"Form initial data: {form.initial}")
    content = {
        'form': form,
        'account': account  # Pass account to template for Cancel button
    }
    return render(request, 'checkbook/UpdateTransaction.html', content) 

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction.Transactions.select_related('account'), pk=pk)
    if request.method == 'POST':
        # determine account pk robustly
        pk_account = getattr(transaction, 'account_id', None) or (transaction.account.pk if getattr(transaction, 'account', None) else None)
        transaction.delete()
        # redirect to euro view for account 2, otherwise regular balance
        if str(pk_account) == '2':
            return redirect('balance2', pk=pk_account)
        return redirect('balance', pk=pk_account)
    content = {'transaction': transaction}
    return render(request, 'checkbook/deleteTransaction.html', content)

@login_required
def update_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = AccountForm(data=request.POST or None, instance=account)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('balance', pk=account.pk)
    content = {'form': form}
    return render(request, 'account/UpdateAccount.html', {'form': form, 'account': account}) #updated case sesitive objects.

@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('index')
    content = {'account': account}
    return render(request, 'account/DeleteAccount.html', content)

@login_required
def reports(request):
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    accounts = Account.Accounts.all()
    chart_data = []

    for account in accounts:
        expenditures = (
            Transaction.Transactions
            .filter(account=account, type='Withdrawal', date__gte=thirty_days_ago)
            .values('category__name')  # Use category name instead of ID
            .annotate(total=Sum('amount'))
        )
        expenditures_list = []
        for exp in expenditures:
            exp_copy = exp.copy()
            if isinstance(exp_copy['total'], Decimal):
                exp_copy['total'] = float(exp_copy['total'])
            # Rename 'category__name' to 'category' for chart compatibility
            exp_copy['category'] = exp_copy.pop('category__name')
            expenditures_list.append(exp_copy)
        chart_data.append({
            'account': account.name,
            'data': expenditures_list
        })

    return render(request, 'checkbook/Reports.html', {
        'chart_data': json.dumps(chart_data)
    })