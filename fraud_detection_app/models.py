from django.db import models

class Person(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    pincode = models.IntegerField()
    mobile_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Account(models.Model):
    id=models.AutoField(primary_key=True)
    balance = models.IntegerField()
    user_id = models.IntegerField()
    account_number = models.CharField(max_length=255)
    ifsc = models.CharField(max_length=255)
    bank_user_id = models.IntegerField()
    nominee = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    logtime = models.DateTimeField(auto_now_add=True)
    from_user_id = models.IntegerField() #user_id of Person or Account
    to_user_id = models.IntegerField()
    from_user_account_id = models.CharField(max_length=255) #account number of sender
    to_user_account_id = models.CharField(max_length=255) # account number of receiver

class FraudCase(models.Model):
    case_id = models.AutoField(primary_key=True)
    description = models.TextField()
    transaction_id = models.IntegerField()
    logtime = models.DateTimeField(auto_now_add=True)
    isfraud = models.BooleanField(default=True)

class userResponse(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    user_id=models.IntegerField()
    rating=models.CharField(max_length=255)
    response=models.TextField()
