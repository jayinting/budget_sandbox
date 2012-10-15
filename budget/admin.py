from django.contrib import admin
from budget.models import (Account, MainCategory, SubCategory, Transaction)

admin.site.register(Account)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Transaction)