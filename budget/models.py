import datetime

from django.db import models
from django.contrib.auth.models import User

from budget import constants as budCon

class BaseModel(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Account(BaseModel):
    user = models.ForeignKey(User)
    currency = models.CharField(max_length=32, choices=budCon.CURRENCY_OPTIONS, default=budCon.CURRENCY_PHP)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Accounts"

    def __unicode__(self):
        """Gets string representation of the model instance"""
        return "%s:%s(%s)" % (self.user.username, self.name, self.currency)

class MainCategory(BaseModel):
    type = models.CharField(max_length=32, choices=budCon.TYPE_OPTIONS, default=budCon.TYPE_EXPENSE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Main Categories"

    def __unicode__(self):
        """Gets string representation of the model instance"""
        return self.name

class SubCategory(BaseModel):
    main_category = models.ForeignKey(MainCategory)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __unicode__(self):
        """Gets string representation of the model instance"""
        return "%s - %s" % (self.main_category.name, self.name)

class Transaction(BaseModel):
    account = models.ForeignKey(Account)
    date = models.DateField(default=datetime.date.today())
    type = models.CharField(max_length=32, choices=budCon.TYPE_OPTIONS, default=budCon.TYPE_EXPENSE)
    category = models.ForeignKey(SubCategory)
    amount = models.FloatField()
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Transactions"

    def __unicode__(self):
        """Gets string representation of the model instance"""
        return "Account(%d):%s" % (self.account.id, self.description)
