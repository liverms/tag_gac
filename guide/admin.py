from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin

import guide.models as models
from guide.models import AGREEMENTS_FIELDS


"""Model resources defines how objects are mapped to their 
import and export representations and handle importing and exporting data.
"""


class ConstructionCoverageResource(resources.ModelResource):


    class Meta:
        model = models.ConstructionCoverage


class GoodsCoverageResource(resources.ModelResource):


    class Meta:
        model = models.GoodsCoverage


class CodeOrganizationExclusionResource(resources.ModelResource):


    class Meta:
        model = models.CodeOrganizationExclusion


class CommodityTypeResource(resources.ModelResource):


    class Meta:
        model = models.CommodityType


class CodeResource(resources.ModelResource):


    class Meta:
        model = models.Code


class GeneralExceptionResource(resources.ModelResource):


    class Meta:
        model = models.GeneralException


class TenderingReasonResource(resources.ModelResource):


    class Meta:
        model = models.LimitedTenderingReason


class CftaExceptionResource(resources.ModelResource):


    class Meta:
        model = models.CftaException


class ValueThresholdResource(resources.ModelResource):


    class Meta:
        model = models.ValueThreshold


class OrganizationResource(resources.ModelResource):


    class Meta:
        model = models.Organization



# ModelAdmins
@admin.register(models.ConstructionCoverage)
class ConstructionCoverageAdmin(ImportExportModelAdmin):
    resource_class = ConstructionCoverageResource
    lst = ['org_fk']
    list_filter = AGREEMENTS_FIELDS
    lst.extend(AGREEMENTS_FIELDS)
    list_display = lst
    list_editable = AGREEMENTS_FIELDS
    list_display_links = ['org_fk']


@admin.register(models.GoodsCoverage)
class GoodsCoverageAdmin(ImportExportModelAdmin):
    resource_class = GoodsCoverageResource
    lst = ['org_fk']
    list_filter = AGREEMENTS_FIELDS
    lst.extend(AGREEMENTS_FIELDS)
    list_display = lst
    list_editable = AGREEMENTS_FIELDS
    list_display_links = ['org_fk']


@admin.register(models.CodeOrganizationExclusion)
class CodeOrganizationExclusionAdmin(ImportExportModelAdmin):
    resource_class = CodeOrganizationExclusionResource
    lst = ['__str__']
    list_filter = AGREEMENTS_FIELDS
    lst.extend(AGREEMENTS_FIELDS)
    list_display = lst
    list_editable = AGREEMENTS_FIELDS
    list_display_links = ['__str__']
    search_fields = ['code_fk__code', 'org_fk__name']


@admin.register(models.CommodityType)
class CommodityTypeAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = CommodityTypeResource


@admin.register(models.Code)
class CodeAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = CodeResource
    lst = ['id', 'code', 'type']
    lst.extend(AGREEMENTS_FIELDS)
    types = ['type']
    types.extend(AGREEMENTS_FIELDS)
    list_filter = types
    search_fields = ['code']
    list_display = lst
    list_editable = list(filter(lambda x: x != 'id', lst))
    list_display_links = ['id']
    ordering = ['code']


@admin.register(models.GeneralException)
class GeneralExceptionAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = GeneralExceptionResource
    lst = ['id', 'name']
    lst.extend(AGREEMENTS_FIELDS)
    list_filter = AGREEMENTS_FIELDS
    search_fields = ['name']
    list_display = lst
    list_editable = list(filter(lambda x: x != 'id', lst))
    list_display_links = ['id']


@admin.register(models.LimitedTenderingReason)
class TenderingReasonAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = TenderingReasonResource
    lst = ['id', 'name']
    lst.extend(AGREEMENTS_FIELDS)
    list_filter = AGREEMENTS_FIELDS
    search_fields = ['name']
    list_display = lst
    list_editable = list(filter(lambda x: x != 'id', lst))
    list_display_links = ['id']


@admin.register(models.CftaException)
class CftaExceptionAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = CftaExceptionResource
    lst = ['id', 'name']
    lst.extend(AGREEMENTS_FIELDS)
    list_filter = AGREEMENTS_FIELDS
    search_fields = ['name']
    list_display = lst
    list_editable = list(filter(lambda x: x != 'id', lst))
    list_display_links = ['id']


@admin.register(models.ValueThreshold)
class ValueThresholdAdmin(ImportExportModelAdmin):
    resource_class = ValueThresholdResource
    lst = ['type']
    list_filter = lst
    list_display_links = lst
    list_display = lst + AGREEMENTS_FIELDS
    list_editable = AGREEMENTS_FIELDS


@admin.register(models.Organization)
class OrganizationAdmin(ImportExportModelAdmin, TranslationAdmin):
    resource_class = OrganizationResource
    lst = ['id', 'name']
    lst.extend(AGREEMENTS_FIELDS)
    list_filter = AGREEMENTS_FIELDS
    search_fields = ['name']
    list_display = lst
    list_editable = list(filter(lambda x: x != 'id', lst))
    list_display_links = ['id']
