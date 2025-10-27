from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from decimal import Decimal, InvalidOperation
import logging

def home(request):
    form = TransactionForm(data=request.POST or None)
    if request.method == 'POST':
        pk = request.POST['account']
        # Route to different balance sheets based on account ID
        if pk == '17':
            return balance2(request, pk)
        else:
            return balance(request, pk)
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
    current_total = account.initial_deposit
    table_contents = {}
    
    # Get transaction IDs first, then fetch each transaction individually
    transaction_ids = Transaction.Transactions.filter(account=pk).order_by('-date').values_list('id', flat=True)
    
    for transaction_id in transaction_ids:
        try:
            t = Transaction.Transactions.select_related().get(id=transaction_id)
            amount = t.amount
            
            if t.type == 'Deposit':
                current_total += amount
                table_contents.update({t: current_total})
            else:
                current_total -= amount
                table_contents.update({t: current_total})
        except (ValueError, TypeError, InvalidOperation, Transaction.DoesNotExist) as e:
            logging.error(f"Error processing transaction {transaction_id}: {str(e)}")
            continue
    
    content = {'account': account, 'table_contents': table_contents, 'balance': current_total}
    return render(request, 'checkbook/BalanceSheet.html', content)

def balance2(request, pk):
    account = get_object_or_404(Account, pk=pk)
    current_total = account.initial_deposit
    table_contents = {}
    
    # Get transaction IDs first, then fetch each transaction individually
    transaction_ids = Transaction.Transactions.filter(account=pk).order_by('-date').values_list('id', flat=True)
    
    for transaction_id in transaction_ids:
        try:
            t = Transaction.Transactions.get(id=transaction_id)
            amount = t.amount
            
            if t.type == 'Deposit':
                current_total += amount
                table_contents.update({t: current_total})
            else:
                current_total -= amount
                table_contents.update({t: current_total})
        except (ValueError, TypeError, InvalidOperation, Transaction.DoesNotExist) as e:
            logging.error(f"Error processing transaction {transaction_id}: {str(e)}")
            continue
    
    content = {'account': account, 'table_contents': table_contents, 'balance': current_total}
    return render(request, 'checkbook/BalanceSheet2.html', content)

def transaction(request):
    form = TransactionForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            
            transaction = form.save()
            print(f"Saved transaction date: {transaction.date}")
            pk = request.POST['account']
            return balance(request, pk)
        else:
            # Debug: Show form errors
            print(f"Form errors: {form.errors}")
    content = {'form': form}
    return render(request, 'checkbook/AddTransaction.html', content)

#make updete and delete views here

def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk) 
    form = TransactionForm(data=request.POST or None, instance=transaction)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
           # Redirect back to the balance sheet for this account
            return redirect('balance', pk=transaction.account.pk)
    else:
        form = TransactionForm(instance=transaction)
         # Debug: Print form data
        print(f"Form date field value: {form['date'].value()}")
        print(f"Form initial data: {form.initial}")
    content = {'form': form}
    return render(request, 'checkbook/UpdateTransaction.html', content) 

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        pk_account = transaction.account.pk
        transaction.delete()
        return balance(request, pk_account)
    # Render confirmation on GET
    content = {'transaction': transaction}
    return render(request, 'checkbook/deleteTransaction.html', content)

#update and delete account views
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