from modeltranslation.translator import TranslationOptions, register

import guide.models as models


"""Provide TranslationOptions with the name of the field
that should be translated and then the required languages.

This automatically takes your models and adds translated fields
For instance in Organization there is a column for the organization 
name (like Fisheries and Oceans).  This will add name_en and name_fr
fields to this model so you end up with 3 name fields.
"""


@register(models.Organization)
class OrganizationTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')


@register(models.CommodityType)
class CommodityTypeTO(TranslationOptions):
    fields = ['commodity_type']
    required_languages = ('en', 'fr')


@register(models.Code)
class CodeTO(TranslationOptions):
    fields = ['code']
    required_languages = ('en', 'fr')


@register(models.LimitedTenderingReason)
class LimitedTenderingReasonTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')


@register(models.GeneralException)
class GeneralExceptionTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')


@register(models.CftaException)
class CftaExceptionTO(TranslationOptions):
    fields = ['name']
    required_languages = ('en', 'fr')
