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
        return fields.Datetime.now()
    
    def _get_default_description(self):
        if self.env.context.get('is_my_property'):
            return "<strong><i>"+self.env.user.name+"</i></strong>'s Property"

    name = fields.Char(help="Estate Name", string="Property Name")
    mobile_no = fields.Char(related='client_id.mobile', string="Mobile No")
    description = fields.Html(string="Estate Details", copy=False, readonly=True, default=_get_default_description)
    address = fields.Char(help="Estate Address", string="Address")
    state = fields.Selection([('prebook', 'Prebook'), ('ready', 'Ready To Be Sold'), ('sold', 'Sold')], string="State")
    client_id = fields.Many2one('estate.client',string="Client", default=lambda self:self.env.user.id)
    price = fields.Float(string="Estate Cost")
    discount = fields.Float(string="Discount(%)", default=0)
    total = fields.Float(compute='_compute_total', inverse='_change_discount', search='_search_total', string='Final Price')
    booking_start = fields.Date(default=fields.Date.today())
    booking_end = fields.Date(states={'ready':[('invisible', 1)]}, string="Prebook End", invisible=0, default= (fields.Date.today() + relativedelta(days=30)))
    # buyer_ids = fields.Many2many(comodel_name='res.partner', relation="estate_estate_buyer_res_partner_many2many", column1="name", column2="display_name", string="Buyer", help="Many2many 2 field with res.partner fetching buyer names", domain="[('is_buyer', '=', 'true')]")
    buyer = fields.Many2one('res.partner' , compute='_get_buyer', store=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

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
    
    def _get_buyer(self):
        for property in self:
            # property.buyer = self.env['estate.property.offer'].browse(self.env['estate.property.offer'].search([('status','=','accepted')], limit=1))
            # Id = self.env['estate.property.offer'].search([('status','=','accepted')], limit=1)
            offer_ids = property.offer_ids
            print("Offer IDS ::: ", offer_ids, ":::", len(offer_ids))
            if offer_ids:
                for offer_id in offer_ids:
                    print("IN Get Buyer :::", property.name, property.buyer, ' ::: ', offer_id.buyer_id)
                    if offer_id and offer_id.status == 'accepted':
                        print("IN Get Buyer :::", offer_id.buyer_id)
                        property.buyer = offer_id.buyer_id
                        print("Done Get Buyer :::", property.buyer)
                        break
                    else:
                        property.buyer = False
            else:
                property.buyer = False
                    
            
class EstateOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Helps you add Offers for buyers"
    
    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected')], copy=False)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.estate', string="Property")
    
    @api.onchange('status')
    def _onchange_status(self):
        # self.ensure_one()
        print("Status ::: ", self.status)
        if self.status == 'accepted':
            print("Accepted ::: ",  self.buyer_id, " :::: ", self.property_id.buyer)
            self.property_id.buyer = self.buyer_id
            print("Accepted ::: ", self.property_id.buyer, " :::: ")
        else:
            self.property_id.buyer = False
            print("Rejected ::: ", self.property_id.buyer)