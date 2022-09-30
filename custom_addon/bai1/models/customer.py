import odoo.exceptions
from odoo import models, fields, api


class Customer(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = []
    discount_code = fields.Char('Discount Code')
    discount_amount = fields.Integer('Discount Amount', compute='_compute_discount_amount')
    valid_discount = fields.Boolean(compute='_valid_discount_compute',
                                    store=True,
                                    invisible=True)

    def _has_valid_discount_code(self):
        self.ensure_one()
        code = str(self.discount_code).split('_')
        if len(code) == 2 and code[0] == 'VIP' and code[1].isdigit():
            if 0 <= int(code[1]) <= 100:
                return True
        return False

    @api.depends('discount_code')
    def _valid_discount_compute(self):
        for sale in self:
            sale.valid_discount = sale._has_valid_discount_code()

    @api.depends('discount_code')
    def _compute_discount_amount(self):
        for customer in self:
            if customer._has_valid_discount_code():
                customer.discount_amount = int(customer.discount_code.split('_')[1])
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

    def update_code_customer(self):
        ids = [x.id for x in self]
        view_id = self.env.ref('bai1.mass_update_customer_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update customer code',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'customer.wizard',
            'target': 'new',
            'context': {
                'default_customer_ids': [(6, 0, ids)],
            }
        }
