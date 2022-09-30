from odoo import models, fields


class CustomerWizard(models.TransientModel):
    _name = 'customer.wizard'

    customer_ids = fields.Many2many('res.partner', string='Customers')
    discount_code = fields.Char('Discount code')

    def update_customers(self):
        for wiz in self:
            for customer in wiz.customer_ids:
                customer.update({
                    'discount_code': wiz.discount_code
                })
