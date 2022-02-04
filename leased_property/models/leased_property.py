from odoo import _, api, fields, models

class leased_property(models.Model):
    _name="leased.property"
    _inherits = {"estate.estate":"property_id"}

    property_id = fields.Many2one('estate.estate')
    lessee_name = fields.Char(string="Lessee Name")
    lease_date = fields.Date(default=fields.Date.today)
    
    def action_save(self):
        for property in self:
            print("Property ;:::", property)
    
    @api.onchange('property_id')
    def _onchange_property_id(self):
        for record in self:
            record.lessee_name = self.env['estate.client'].search([('id','=',record.client_id.id)], limit=1).user_id.name