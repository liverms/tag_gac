
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from guide.views import (FORMS, CodeAutocomplete, EntitiesAutocomplete,
                         OpenPDF, TradeForm, TypeAutocomplete, done_step_name,
                         lt_condition, url_name)

#This is required to conditionally render the limited tendering form.
trade_wizard = TradeForm.as_view(
    FORMS, 
    condition_dict={"3": lt_condition}, 
    url_name=url_name, 
    done_step_name=done_step_name
)
app_name='guide'
urlpatterns = [
    path('entities_autocomplete/', EntitiesAutocomplete.as_view(), name='entities_autocomplete'),
    path('type_autocomplete/', TypeAutocomplete.as_view(), name='type_autocomplete'),
    path('code_autocomplete/', CodeAutocomplete.as_view(), name='code_autocomplete'),
    path('open_pdf/', OpenPDF.as_view(), name='open_pdf'),
    path('form/<step>/', trade_wizard, name='form_step'),
    path('form/done/', trade_wizard, name='done_step'),
    re_path('form/', RedirectView.as_view(url='0/'), name='form_start'),
    re_path('', RedirectView.as_view(url='form/0/')),
    re_path(r'^.*$', RedirectView.as_view(url='form/0/')),
    re_path(r'^.*/$', RedirectView.as_view(url='form/0/'))
]
