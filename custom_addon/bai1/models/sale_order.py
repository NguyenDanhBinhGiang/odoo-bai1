import odoo.exceptions
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_discounted = fields.Float('Discounted Total', compute='_amount_all')
    discount_code = fields.Char('Discount code', related='partner_id.discount_code', readonly=False)

    @api.depends('order_line.price_total', 'partner_id')
    def _amount_all(self):
        super(SaleOrder, self)._amount_all()
        for sale in self:
            sale.amount_discounted = sale.amount_total * sale.partner_id.discount_amount / 100 * -1
            sale.amount_total = sale.amount_total + sale.amount_discounted

