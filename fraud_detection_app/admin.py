from django.contrib import admin
from fraud_detection_app.models import Person, Account, Transaction, FraudCase
# Register your models here.

admin.site.register(Person)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(FraudCase)