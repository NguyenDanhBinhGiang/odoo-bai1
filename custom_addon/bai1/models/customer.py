import odoo.exceptions
from odoo import models, fields, api


class Customer(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = []
    discount_code = fields.Char('Discount Code')
    discount_amount = fields.Integer('Discount Amount', compute='_compute_discount_amount')

    @api.constrains('discount_code')
    def _check_valid_discount_code(self):
        for customer in self:
            code = str(customer.discount_code).split('_')
            if not (len(code) == 2 and code[0] == 'VIP' and code[1].isdigit() and 0 <= int(code[1]) <= 100):
                raise odoo.exceptions.UserError('Discount code is not valid')

    @api.depends('discount_code')
    def _compute_discount_amount(self):
        for customer in self:
            if customer.discount_code:
                customer.discount_amount = int(str(customer.discount_code).split('_')[1])
                if customer.discount_amount < 0 or customer.discount_amount > 100:
                    customer.discount_amount = 0
            else:
                customer.discount_amount = 0

    def create(self, vals_list):
        if not self.user_has_groups('bai1.advanced_sale'):
            if 'discount_code' in vals_list:
                raise odoo.exceptions.UserError('You do not have permission!')
        return super(Customer, self).create(vals_list=vals_list)

    def write(self, vals):
        if not self.user_has_groups('bai1.advanced_sale'):
            if 'discount_code' in vals:
                raise odoo.exceptions.UserError('You do not have permission!')
        return super(Customer, self).write(vals=vals)


