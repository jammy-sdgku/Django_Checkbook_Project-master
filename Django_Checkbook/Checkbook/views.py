from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from decimal import Decimal, InvalidOperation
import logging
from django.core.paginator import Paginator

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


def create_account(request):
    form = AccountForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')
    content = {'form': form}
    return render(request, 'checkbook/CreateNewAccount.html', content)


def balance(request, pk):
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

def transaction(request):
    form = TransactionForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            tx = form.save()
            print(f"Saved transaction date: {tx.date}")
            # determine account pk robustly (use tx.account_id if available)
            pk = getattr(tx, 'account_id', None) or request.POST.get('account')
            # redirect to the euro view for account 17, otherwise regular balance
            if str(pk) == '17':
                return redirect('balance2', pk=pk)
            return redirect('balance', pk=pk)
        else:
            print(f"Form errors: {form.errors}")
    content = {'form': form}
    return render(request, 'checkbook/AddTransaction.html', content)

def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction.Transactions.select_related('account'), pk=pk) 
    form = TransactionForm(data=request.POST or None, instance=transaction)
    if request.method == 'POST':
        if form.is_valid():
            updated = form.save()
            # determine the account pk after save (account may have been changed)
            account_pk = getattr(updated, 'account_id', None) or (updated.account.pk if getattr(updated, 'account', None) else None)
            # Redirect to the euro view for account 17, otherwise regular balance
            if str(account_pk) == '17':
                return redirect('balance2', pk=account_pk)
            return redirect('balance', pk=account_pk)
    else:
        form = TransactionForm(instance=transaction)
        print(f"Form date field value: {form['date'].value()}")
        print(f"Form initial data: {form.initial}")
    content = {'form': form}
    return render(request, 'checkbook/UpdateTransaction.html', content) 

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction.Transactions.select_related('account'), pk=pk)
    if request.method == 'POST':
        # determine account pk robustly
        pk_account = getattr(transaction, 'account_id', None) or (transaction.account.pk if getattr(transaction, 'account', None) else None)
        transaction.delete()
        # redirect to euro view for account 17, otherwise regular balance
        if str(pk_account) == '17':
            return redirect('balance2', pk=pk_account)
        return redirect('balance', pk=pk_account)
    content = {'transaction': transaction}
    return render(request, 'checkbook/deleteTransaction.html', content)

def update_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = AccountForm(data=request.POST or None, instance=account)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('index')
    content = {'form': form}
    return render(request, 'account/UpdateAccount.html', content)

def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        return redirect('index')
    content = {'account': account}
    return render(request, 'account/DeleteAccount.html', content)