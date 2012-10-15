from django.views.generic import (TemplateView   )

class Index_View(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Index_View, self).get_context_data(**kwargs)

        return context