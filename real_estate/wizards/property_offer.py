from odoo import fields,models

class PropertyOffer(models.TransientModel):
    _name = "estate.property.offer.wizard"
    
    buyer_ids = fields.Many2many('res.partner', string="Buyers", column1="name", column2="display_name", domain="[('is_buyer', '=', 'true')]")
    offer = fields.Integer(string="Price")
    property_id = fields.Many2one('estate.estate', string="Property")
    
    def property_offer_wizard_action(self):
        
        pass