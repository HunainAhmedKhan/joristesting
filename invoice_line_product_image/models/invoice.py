# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
class AccountMove(models.Model):
    _inherit = "account.move"

    contact_name =fields.Many2one("res.partner",string="ATTN", domain="[('id', 'child_of', partner_id)]")
    shipment_term = fields.Many2one("account.payment.term", string="Shipping Terms")
    method = fields.Many2one("utm.source", string="Shipping Method")
    estimated_date = fields.Date(string="Estimated Shipment Date")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'invoice_line_ids' in vals:
                vals['line_ids'] = vals.pop('invoice_line_ids')
        return super(AccountMove, self.with_context(check_move_validity=False)).create(vals_list)

    def write(self, vals):
        if 'invoice_line_ids' in vals:
            vals['line_ids'] = vals.pop('invoice_line_ids')
        return super(AccountMove, self.with_context(check_move_validity=False)).write(vals)



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    po_number = fields.Char(string="PO#")
    customer_number = fields.Many2one("res.partner", string="Customer#")
    item_number = fields.Many2one("res.partner", string="Item #")
    image_128 = fields.Image(string="Image",compute="_onchange_product_images")

    customer_no = fields.Char(string="Customer No", compute="_onchange_customer_no")

    @api.depends('product_id')
    def _onchange_product_images(self):
        for line in self:
            line.image_128 = line.product_id.image_128

    @api.depends('product_id')
    def _onchange_customer_no(self):
        for line in self:
            proObj=self.env['product.product'].search([('id','=',line.product_id.id),('online_marketing.customer_id', '=',line.move_id.partner_id.id)],limit=1)
            line.customer_no = proObj.online_marketing.customer_no


class ResPartner(models.Model):
    _inherit = "res.partner"

    shipping = fields.Char('WareHouse Name')
    contact_id = fields.Char('Contact Id')
    extra_11 = fields.Char('extra 1')
    extra_21 = fields.Char('extra 2')
    extra_31 = fields.Char('extra 3')



class education_history(models.Model):
    _inherit = 'product.template'

    item_no = fields.Char(string='Item No',help="Item No")
    customer_no = fields.Char(string='Customer No')
    hs_code = fields.Char(string='HS Code')
    online_marketing = fields.One2many('product.identifier', 'omtask_id', string='Identifier')

class OnlineMarketing(models.Model):
    _name = 'product.identifier'

    omtask_id = fields.Many2one("product.template")
    customer_id = fields.Many2one("res.partner",string='Customer')
    customer_no = fields.Char(string="Customer Item #")

