import shipper
from livesettings import config_choice_values

def get_methods():
    return [shipper.Shipper(service_type=value) for value in config_choice_values('satchmo_indiapost', 'SHIPPING_CHOICES')]
