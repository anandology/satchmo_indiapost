from django.utils.translation import ugettext_lazy as _
from livesettings import *

SHIP_MODULES = config_get('SHIPPING', 'MODULES')
SHIP_MODULES.add_choice(('satchmo_indiapost', 'India Post'))

SHIPPING_GROUP = ConfigurationGroup('satchmo_indiapost',
  _('India Post Shipping Settings'),
  requires = SHIP_MODULES,
  requiresvalue='satchmo_indiapost',
  ordering = 101
)

config_register_list(    
    MultipleStringValue(SHIPPING_GROUP,
        'SHIPPING_CHOICES',
        description=_('Shipping Choices Available to customers.'),
        choices = (
                    (('REG_PARCEL','Registered Parcel')),
                    (('REG_PARCEL_VPP','Registered Parcel - Payment on Delivery')),
                    (('REG_BOOKPOST','Registered Book Post')),
                    (('REG_BOOKPOST_VPP','Registered Book Post - Payment on Delivery')),
        ),
        default = ('REGBOOKPOST_VPP',)),
    
    BooleanValue(SHIPPING_GROUP,
        'VERBOSE_LOG',
        description=_("Verbose logs"),
        help_text=_("Send the entire request and response to the log - for debugging help when setting up IndiaPost."),
        default=False)
)
