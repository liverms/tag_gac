from django.db import models
from django.utils.translation import gettext_lazy as _

TYPE_CHOICES = [('1', 'GOODS'), 
                ('2', 'SERVICES'), 
                ('3', 'CONSTRUCTION')]

AGREEMENTS = (
    _('CCFTA'), 
    _('CCoFTA'), 
    _('CHFTA'), 
    _('CPaFTA'), 
    _('CPFTA'), 
    _('CKFTA'), 
    _('CUFTA'), 
    _('WTO-AGP'),
    _('CETA'), 
    _('CPTPP'), 
    _('CFTA')
)

AGREEMENTS_FIELDS = [field.replace('-', '_').lower() for field in AGREEMENTS]


class BooleanTradeAgreement(models.Model):
    """This abstract model will be inherited by most
    other models which will appear as a true or false
    option for each trade agreement in those models.

    Args:
        models ([class]): Model class
    """

    id = models.AutoField(primary_key=True)
    ccfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[0],
        blank = False
    )
    ccofta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[1],
        blank = False
    )
    chfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[2],
        blank = False
    )
    cpafta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[3],
        blank = False
    )
    cpfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[4],
        blank = False
    )
    ckfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[5],
        blank = False
    )
    cufta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[6],
        blank = False
    )
    wto_agp = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[7],
        blank = False
    )
    ceta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[8],
        blank = False
    )
    cptpp = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[9],
        blank = False
    )
    cfta = models.BooleanField(
        default = False,
        verbose_name = AGREEMENTS[10],
        blank = False
    )


    class Meta:
        abstract = True


class Organization(BooleanTradeAgreement):
    """Model for organizations with a boolean (inherited)
    to indicate if the org is covered by a trade agreement
    or not.

    Args:
        BooleanTradeAgreement ([class]): Model Clas

    Returns:
        [str]: Str of model instance
    """
    name = models.CharField(
        max_length = 250,
        default = '',
        unique = True,
        verbose_name = _('Entities')
    )


    class Meta:
        ordering = ['name']
        verbose_name_plural = "  Entities" # 2 space, easy way to arrange model order in admin
    
    def __str__(self):
        return self.name


class CommodityType(models.Model):
    """Model for commodity types, goods, services, construction

    Args:
        models ([class]): Model class

    Returns:
        [str]: Instance name
    """
    c_type = models.CharField(
        choices=TYPE_CHOICES,
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Commodity Type')
    )
    commodity_type = models.CharField(
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Commodity Type')
    )


    class Meta:
        ordering = ['commodity_type']
        verbose_name_plural = "  Commodity Types" # 2 space
 
    def __str__(self):
        return self.commodity_type


class Code(BooleanTradeAgreement):
    """Commodity codes with a foreign key of commodity
    type so each code is associated with a type.  Inherits
    booleantradeagreement so that each code can have a bool 
    to indicate if it applies or not to each agreement.

    Args:
        BooleanTradeAgreement ([class]): Model class

    Returns:
        [str]: Str of instance code
    """
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )
    code = models.CharField(
        max_length = 128,
        default = '',
        unique = True,
        verbose_name = _('Code')
    )

    def __str__(self):
        return self.code
    class Meta:
        verbose_name_plural = " Commodity Codes" # 1 space


class ConstructionCoverage(BooleanTradeAgreement):
    """Model for organizations for which no construction codes
    are covered.  Inherits booleantradeagreement so that you 
    can indicate which agreements have this exception

    Args:
        BooleanTradeAgreement ([class]): Model class

    Returns:
        [str]: Str of org foreign key
    """
    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        verbose_name = _('Org fk'),
        on_delete = models.CASCADE
    )


    class Meta:
        verbose_name_plural = "Construction Coverage" # 0 space

    def __str__(self):
        return str(self.org_fk)


class GoodsCoverage(BooleanTradeAgreement):
    """For most organizations ALL goods are covered
    by the agreement.  However, for some organizations
    there is a mixed list with some goods covered and 
    some are not covered.  This is usually DND, RCMP, 
    and Coast Guard

    Args:
        BooleanTradeAgreement ([class]): Model Class

    Returns:
        [str]: Str of org fk
    """
    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        verbose_name = _('Org fk'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return str(self.org_fk)
    

    class Meta:
        verbose_name_plural = "Goods Coverage" # 0 space


class CodeOrganizationExclusion(BooleanTradeAgreement):
    """This implements a trade rule that is a big complicated.
    In some agreements there is a carveout that says for
    Department X the Commodity Code Y is not covered. Usually
    commodity codes are covered or not covered for all entities
    in an agreement.

    The content for this is stored in the CodeOrganizationExclusion
    model.  This stores the Dept and Commodity code and inherits 
    boolean trade agreement so that you can indicate in which 
    agreements this rule is found. Indicate true for those
    agreements in which it is found.

    Args:
        BooleanTradeAgreement ([class]): Model class

    Returns:
        [str]: string
    """
    code_fk = models.ForeignKey(
        Code,
        to_field = 'code',
        related_name = '+',
        verbose_name = _('Code FK en ca'),
        on_delete = models.CASCADE
    )
    org_fk = models.ForeignKey(
        Organization,
        to_field = 'name',
        related_name = '+',
        verbose_name = _('Org fk en ca'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return f"{self.org_fk} - {self.code_fk} - Exclusion"


    class Meta:
        verbose_name_plural = "Commodity Code - Entities - Exclusions" # 0 space


class ValueThreshold(models.Model):
    """Each trade agreement has trade thresholds.  Above these thresholds the trade
    agreement applies, below this threshold the trade agreement does not apply.
    There are different thresholds for each agreement, and within each agreement there
    are different thresholds for each commodity type (Goods, Services, Construction).

    Args:
        models ([class]): Model Class

    Returns:
        [str]: Commodity type
    """
    id = models.AutoField(primary_key = True)
    ccfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[0],
        blank = False
    )
    ccofta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[1],
        blank = False
    )
    chfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[2],
        blank = False
    )
    cpafta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[3],
        blank = False
    )
    cpfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[4],
        blank = False
    )
    ckfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[5],
        blank = False
    )
    cufta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[6],
        blank = False
    )
    wto_agp = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[7],
        blank = False
    )
    ceta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[8],
        blank = False
    )
    cptpp = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[9],
        blank = False
    )
    cfta = models.PositiveIntegerField(
        default = 0,
        verbose_name = AGREEMENTS[10],
        blank = False
    )

    type = models.ForeignKey(
        CommodityType,
        to_field = 'commodity_type',
        related_name = '+',
        max_length = 128,
        default = '',
        verbose_name = _('Commodity Type'),
        on_delete = models.CASCADE
    )

    def __str__(self):
        return str(self.type)


    class Meta:
        verbose_name_plural = "  Value Thresholds" # 2 space


class LimitedTenderingReason(BooleanTradeAgreement):
    """Each trade agreement contains a list of reasons a procurement
    officer may use to limit the duration required to solicit bids.

    This model has a list of limited tendering reasons, and inherits
    from booleantradeagreement so you can indicate for which trade
    agreement each exception applies.

    Args:
        BooleanTradeAgreement ([class]): Model clas

    Returns:
        [str]: Str of instance
    """
    name = models.TextField(
        default = '',
        unique = True,
        verbose_name = _('Description')
    )

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = "  Limited Tendering Reasons" # 2 space


class GeneralException(BooleanTradeAgreement):
    """Each trade agreement has a list of general exceptions.  If
    a procurement officer decides that a given exception applies
    to a procurement, then the trade agreements that have that
    exception do not apply to that procurement.

    Args:
        BooleanTradeAgreement ([class]): Model class

    Returns:
        [str]: Str of instance
    """
    name = models.TextField(
        default = '',
        unique = True,
        verbose_name = _('Description')
    )
    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "  General Exceptions" # 2 space


class CftaException(BooleanTradeAgreement):
    """The CFTA has exceptions that are not found
    in Canada's international trade agreements.

    If one of these exceptions applies to a procurement
    then the procurement is not covered by the CFTA.

    Args:
        BooleanTradeAgreement ([class]): Model class

    Returns:
        [str]: Str of instance
    """
    name = models.TextField(
        default = '',
        unique = True,
        verbose_name = _('Description')
    )

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "  CFTA Exceptions" # 2 space
