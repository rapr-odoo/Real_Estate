from odoo import fields,models

class PropertyOffer(models.TransientModel):
    _name = "estate.property.offer"
    
    buyer_ids = fields.Many2many('res.partner', string="Buyers", column1="name", column2="display_name", domain="[('is_buyer', '=', 'true')]")