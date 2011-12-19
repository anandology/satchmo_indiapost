# satchmo-indiapost

satchmo-indiapost is a python module to use India Post for shipping.

To enable this, add `satchmo_indiapost` to `CUSTOM_SHIPPING_MODULES` setting in `settings.py`.

	SATCHMO_SETTINGS = {
		...,
	    'CUSTOM_SHIPPING_MODULES': ['satchmo_indiapost']
	}

Currently this supports "Registered Book Post", "Registered Book Post VPP". Support for other delivery methods is planned.

The post charges are calulated in the code, without making any network calls. 
The calculation is based on the [tariff calculator][] on the India Post website.

[tariff calculator]: http://www.indiapost.gov.in/Netscape/Domestic.html

