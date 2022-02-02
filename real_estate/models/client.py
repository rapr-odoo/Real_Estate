from odoo import _, api, fields, models
from odoo.exceptions import UserError

class client(models.Model):
    _name = "estate.client"
    _rec_name = "user_id"
    mobile = fields.Char(help="Enter Your Mobile Number")
    user_id = fields.Many2one('res.users', string="Client Name")
    property_ids = fields.One2many('estate.estate','client_id', string="Properties")
    total_assets = fields.Float(compute='_compute_total_assets')
    

    @api.depends('property_ids.price','property_ids.discount')
    def _compute_total_assets(self):
        for record in self:
            total = 0
            for client in record.property_ids:
                total += client.total
            record.total_assets = total

    @api.constrains('mobile')
    def _check_mobile(self):
        if self.mobile:
            if not self.mobile.isdigit() or len(self.mobile) != 10:
                raise UserError(_('Enter a valid 10 digit Mobile Number'))

    @api.constrains('partner_id')
    def _check_partner_id(self):
        if self.partner_id:
            self.env.cr.execute(f"SELECT id FROM estate_client WHERE partner_id = '{self.partner_id.id}' FETCH FIRST 1 ROWS ONLY")
            res = self.env.cr.fetchall()
            if len(res) > 1:
                raise UserError(_('Client Name should be unique'))