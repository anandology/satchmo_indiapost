from decimal import Decimal
from django.utils.translation import ugettext as _

from shipping.modules.base import BaseShipper

import logging
import math

log = logging.getLogger('indiapost.shipper')

class Shipper(BaseShipper):
    def __init__(self, cart=None, contact=None, service_type=None):
        print "Shipper", service_type
        self.cart = cart
        self.contact = contact
        self.service_type = service_type
        
        if service_type:    
            self.service_type_code = service_type[0]
            self.service_type_text = service_type[1]
        else:
            self.service_type_code = '99'
            self.service_type_text = 'Uninitialized'
        self.charges = None            
        # Had to edit this so the shipping name did not error out for being more than 30 characters. Old code is commented out.
        #self.id = u'FedEx-%s-%s' % (self.service_type_code, self.service_type_text)
        self.id = u'%s' % (self.service_type_code)
                
    def description(self):
        """
        A basic description that will be displayed to the user when selecting their shipping options
        """
        return self.service_type_text

    def cost(self):
        """
        Complex calculations can be done here as long as the return value is a decimal figure
        """
        assert self.charges is not None
        return Decimal(str(self.charges))

    def method(self):
        """
        Describes the actual delivery service (Mail, FedEx, DHL, UPS, etc)
        """
        return _("India Post")

    def expectedDelivery(self):
        """
        Can be a plain string or complex calcuation returning an actual date
        """
        return _("7 business days")

    def valid(self, order=None):
        """
        Can do complex validation about whether or not this option is valid.
        For example, may check to see if the recipient is in an allowed country
        or location.
        """
        return True

    def calculate(self, cart, contact):
        weight, price = self._compute_total_weight_price(cart)

        if self.service_type_code == 'REG_BOOKPOST':
            postage = math.ceil(weight/100.0)  # Rs. 1 for 100g
            reg_fee = 17 # Fixed fee of Rs. 17
            self.charges = postage + reg_fee
        elif self.service_type_code == "REG_BOOKPOST_VPP":
            # Rs. 1 for 100g + Rs. 17 for registration fee
            postage = math.ceil(weight/100.0)  # Rs. 1 for 100g
            # special concession for bookpost-vpp if price is less than 50.
            if price <= 20:
                reg_fee = 2.50
            elif price <= 50:
                reg_fee = 2.50
            else:
                reg_fee = 17
            vpp_fee = self._vpp_fee(price)
            self.charges = postage + reg_fee + vpp_fee
        elif self.service_type_code == 'REG_PARCEL':
            # Rs. 19 for first 500g and Rs. 16 for every 500g thereafter.
            n = math.ceil(weight/500.0)
            postage = 19 + (n-1) * 16
            reg_fee = 17
            self.charges = postage + reg_fee
        elif self.service_type_code == 'REG_PARCEL_VPP':
            # Rs. 19 for first 500g and Rs. 16 for every 500g thereafter.
            n = math.ceil(weight/500.0)
            postage = 19 + (n-1) * 16
            reg_fee = 17
            
            if price <= 20:
                vpp_fee = 2
            elif price <= 50:
                vpp_fee = 3
            else:
                vpp_fee = 5
            self.charges = postage + reg_fee + vpp_fee
            
    def _vpp_fee(self, price):
        if price <= 20:
            return 2.0
        elif price <= 50:
            return 3.0
        else:
            return 5.0
        
    def _compute_total_weight_price(self, cart):
        """Computes the total weight and total price.
        Assumes that the weight is in grams.
        """
        box_price = 0
        box_weight = 0
        for product in cart.get_shipment_list():
            box_price += product.unit_price
            if product.weight is None:
                log.warn("No weight on product (skipping for ship calculations): %s", product)
            else:
                box_weight += product.weight
                
        return float(box_weight), float(box_price)
