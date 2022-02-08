from odoo import http
from odoo.http import request

class RealEstate(http.Controller):

    @http.route('/hello', auth="public")
    def hello(self, **kw):
        return "Hello World"

    @http.route('/hello_user', auth="user")
    def hello_user(self, **kw):
        return "Hello %s" %(request.env.user.name)

    @http.route('/hello_template')
    def hello_template(self, **kw):
        return request.render('real_estate.hello_world')

    @http.route('/hello_template_user')
    def hello_template_user(self, **kw):
        clients = request.env['estate.client'].search([])
        print ("courses ::: ", clients)
        return request.render('real_estate.hello_user', { 'user': request.env.user, 'clients': clients })

    @http.route(['/client', '/client/static/<string:is_static>'], auth="public", website=True)
    def courses(self, is_static=False, **kw):
        if is_static:
            return request.render('real_estate.clients_static', {
                'clients': request.env['estate.client'].sudo().search([], limit=8)
            })
        return request.render('real_estate.clients', {
                'clients': request.env['estate.client'].sudo().search([], limit=8)
            })

    @http.route(['/client/<model("estate.client"):client>', '/client/<string:is_static>'], auth="public", website=True)
    def course_details(self, client=False, **kw):
        if client:
            return request.render('real_estate.client_details', {
                'client': client,
            })
        