import  csv
from django.views.generic import (TemplateView, FormView  )
from django.core.urlresolvers import reverse
from django.db.models import Sum

from budget import models as budMod
from budget import constants as budCon
from budget import forms as budForm

class Index_View(TemplateView):
    template_name = "budget/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Index_View, self).get_context_data(**kwargs)

        account = budMod.Account.objects.get(pk=1)
        income = budMod.Transaction.objects.filter(account=account, type=budCon.TYPE_INCOME).aggregate(total=Sum('amount'))
        expenses = budMod.Transaction.objects.filter(account=account, type=budCon.TYPE_EXPENSE).aggregate(total=Sum('amount'))

        print income.get('total') - expenses.get('total')

        return context

class Import_Csv(FormView):
    form_class = budForm.SampleForm
    template_name = "budget/form.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Import_Csv, self).get_context_data(**kwargs)

        user = self.request.user
        accounts = budMod.Account.objects.filter(user=user).all().order_by('created')
        context['accounts'] = accounts

        return context

    def get_success_url(self):

        return reverse('budget:Import_Csv')

    def form_valid(self, form):

        account = budMod.Account.objects.get(pk=int(form.data.get('account')))
        self.account = account

        csvData = {}
        try:
            csvData = csv.DictReader(form.cleaned_data.get('file',None))
            budMod.Transaction.objects.filter(account=self.account).delete()
        except Exception:
            pass

        for line in csvData:
            self.process_row(line)

        return super(Import_Csv, self).form_valid(form)

    def process_row(self, row):
        category_str = row.get('Category', 'N/A') if row.get('Category', 'N/A') != '' else 'N/A'
        subcategory_str = row.get('Subcategory', 'N/A') if row.get('Subcategory', 'N/A') != '' else 'N/A'
        amount_float = float(row.get('Amount', '0') if row.get('Amount', '0') != '' else '0')

        type = budCon.TYPE_EXPENSE if (float(row.get('Amount')) <= 0) else budCon.TYPE_INCOME
        date = row.get('Date')
        category, created = budMod.MainCategory.objects.get_or_create(name=category_str)
        subcategory, created = budMod.SubCategory.objects.get_or_create(name=subcategory_str, main_category=category)
        amount = amount_float if (amount_float >= 0) else (amount_float * (-1))
        description = row.get('Description', 'N/A') if row.get('Category', 'N/A') != '' else 'N/A'

        budMod.Transaction.objects.create(account=self.account, type=type, category=subcategory, amount=amount, description=description, date=date)

        #print type, " ", category.name, " ", subcategory.name, " ", amount, " ", description