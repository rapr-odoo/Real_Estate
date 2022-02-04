from odoo import _, api, fields, models
from odoo.exceptions import UserError

class EstateOffer(models.TransientModel):
    _name = "estate.estate.apply.offer.wizard"
    
    discount = fields.Float(string="Discount (%)")
    
    @api.constrains('discount')
    def _constrains_discount(self):
        self.ensure_one()
        if self.discount > 100:
            raise UserError(_("Discount can't be more than 100%"))
        elif self.discount < 0:
            raise UserError(_("Discount can't be less than 0%"))
        
    def action_apply_offer(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids')
        self.env['estate.estate'].browse(active_ids).write({'discount':self.discount})
        pass