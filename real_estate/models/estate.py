from email.policy import default
from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class estate(models.Model):
    _name = "estate.estate"

    def get_default_user_name(self):
        return self.env.user.name

    def _get_default_date(self):
        return fields.Datetime.now()

    def _get_default_end_date(self):
        import pdb
        pdb.set_trace()
        return fields.Datetime.now()
    
    def _get_default_description(self):
        if self.env.context.get('is_my_property'):
            return "<strong><i>"+self.env.user.name+"</i></strong>'s Property"

    name = fields.Char(help="Estate Name", string="Property Name")
    mobile_no = fields.Char(related='client_id.mobile', string="Mobile No")
    description = fields.Html(string="Estate Details", copy=False, readonly=True, default=_get_default_description)
    address = fields.Char(help="Estate Address", string="Address")
    state = fields.Selection([('ready', 'Ready To Be Sold'), ('construction', 'Under Construction'), ('prebook', 'Prebook')], string="State")
    client_id = fields.Many2one('estate.client',string="Client", default=lambda self:self.env.user.id)
    price = fields.Float(string="Estate Cost")
    discount = fields.Float(string="Discount(%)", default=0)
    total = fields.Float(compute='_compute_total', inverse='_change_discount', search='_search_total', string='Final Price')
    booking_start = fields.Date(default=fields.Date.today())
    booking_end = fields.Date(states={'ready':[('invisible', 1)]}, string="Prebook End", invisible=0, default= (fields.Date.today() + relativedelta(days=30)))
    buyer_ids = fields.Many2many(comodel_name='res.partner', relation="estate_estate_buyer_res_partner_many2many", column1="name", column2="display_name", string="Buyer", help="Many2many 2 field with res.partner fetching buyer names", domain="[('is_buyer', '=', 'true')]")

    @api.onchange('booking_start')
    def _change_booking_end(self):
        for record in self:
            if record.booking_end:
                record.booking_end = record.booking_start + relativedelta(days=30)
    
    @api.constrains('booking_start', 'booking_end')
    def _check_diff_date(self):
        for record in self:
            if record.booking_start >= record.booking_end:
                raise UserError(_('Booking Start and Booking End date should be different and Booking Start Date can\'t be less than booking End date'))

    @api.depends('price','discount')
    def _compute_total(self):
        for estate in self:
            try:
                estate.total = estate.price - (estate.price * estate.discount / 100)
            except ZeroDivisionError as e:
                print("Zero Division")
    
    def _change_discount(self):
        for estate in self:
            try:
                estate.discount = (estate.price - estate.total) * 100 / estate.price
            except ZeroDivisionError as e:
                print("[x] Error: Zero Division!!!")
    
    def _search_total(self, operator, value):
        self.env.cr.execute(f"SELECT id FROM estate_estate WHERE (price - (price * discount / 100)) {operator} {value}")
        ids = self.env.cr.fetchall()
        return [('id', 'in', ids)]

    def _search_name(self, *args):
        return [('user_name', 'in', self.env.user.name)]

    def _get_user_name(self):
        for record in self:
            record.user_name = self.env.user.name