from email.policy import default
from odoo import models, fields

class ResPartnerExtended(models.Model):
    _inherit = "res.partner"
    
    is_buyer = fields.Boolean(string = "Buyer", default="false")