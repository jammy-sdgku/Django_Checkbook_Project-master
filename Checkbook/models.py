from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    initial_deposit = models.DecimalField(max_digits=15, decimal_places=2)

    Accounts = models.Manager()
    def __str__(self):
        return self.name + ' ' + self.account_number


TransactionTypes = [('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')]

class category(models.Model):
    name = models.CharField(max_length=50)

    Categories = models.Manager()

    def __str__(self):
        return self.name
    
CategoryTypes = [('House', 'House'), ('Work', 'Work'), ('Education', 'Education'), ('Entertainment/Dining', 'Entertainment/Dining'), ('Auto', 'Auto'), ('Bank', 'Bank'), ('Transfer', 'Transfer'), ('Misc', 'Misc')]

class Transaction(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TransactionTypes)
    to_from = models.CharField(max_length=100, default='none')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100)
    cleared = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    Transactions = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['account', '-date']),  # Optimize the filter + order_by
        ]