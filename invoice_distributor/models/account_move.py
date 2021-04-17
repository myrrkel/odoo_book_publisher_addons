# -*- coding: utf-8 -*-
# Copyright (C) 2020 - myrrkel (https://github.com/myrrkel).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import pycompat
import base64
import io
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_distributor = fields.Boolean("Distributor Invoice", related='partner_id.is_distributor')
    distributor_order_name = fields.Char('Order Name', compute='_compute_distributor_order_name')

    def _compute_distributor_order_name(self):
        self.distributor_order_name = 'DOR/%s' % str(self.id).zfill(5)

    def action_post(self):
        res = super(AccountMove, self).action_post()

        for invoice in self.filtered(lambda inv: inv.partner_id.is_distributor):
            _logger.info("Distributor Invoice %s", invoice.name)

            invoice_lines = invoice.mapped('invoice_line_ids').filtered(lambda line: line.partner_id
                                                                        and line.product_id.type == 'product')
            for invoice_line in invoice_lines:
                if invoice_line.sale_line_ids:
                    # Update new quantity
                    for sale_line in invoice_line.sale_line_ids:
                        if invoice_line in sale_line.invoice_lines:

                            for move_line in sale_line.move_ids:
                                move_line.product_uom_qty = invoice_line.quantity
                                move_line.quantity_done = invoice_line.quantity

                            sale_line.product_uom_qty = invoice_line.quantity
                    continue

                # Create sale order and confirmed picking for the account move line
                _logger.info("Invoice Line %s %s", invoice_line.product_id.name, invoice_line.customer_id.name)
                m_sale_order = self.env['sale.order']
                order = m_sale_order.create({'partner_id': invoice_line.customer_id.id,
                                             'partner_invoice_id': invoice_line.partner_id.id,
                                             'warehouse_id': invoice.partner_id.location_id.get_warehouse().id,
                                             'state': 'sale',
                                             })

                order_line = self.env['sale.order.line'].create({'order_id': order.id,
                                                                 'product_id': invoice_line.product_id.id,
                                                                 'product_uom_qty': invoice_line.quantity,
                                                                 'invoice_lines': [(6, 0, [invoice_line.id])]
                                                                 })

                picking = order.picking_ids[0]
                picking.action_confirm()
                picking.move_lines.quantity_done = invoice_line.quantity
                picking.action_done()

        return res

    def action_distributor_order_send(self):
        """ Opens a wizard to compose an email ans send distributor order """
        self.ensure_one()
        template_id = self.env['ir.model.data'].xmlid_to_res_id('invoice_distributor.email_template_distributor_order',
                                                                raise_if_not_found=False)

        data_record = self.distributor_order_to_csv()
        ir_values = {
            'name': "%s.csv" % self.distributor_order_name.replace('/', '_'),
            'type': 'binary',
            'datas': base64.encodebytes(data_record),
            'mimetype': 'text/csv',
        }
        csv_attach_id = self.env['ir.attachment'].create(ir_values)

        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        template.attachment_ids = [(6, 0, [csv_attach_id.id])]
        if template.lang:
            lang = template._render_template(template.lang, 'account.move', self.ids[0])
        ctx = {
            'default_model': 'account.move',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def distributor_order_to_csv(self):
        csv_fields = [(_('Customer'), 'customer'),
                      (_('Street'), 'street'),
                      (_('Street2'), 'street2'),
                      (_('City'), 'city'),
                      (_('Zip Code'), 'zip'),
                      (_('Country'), 'country'),
                      (_('Product'), 'product'),
                      (_('Barcode'), 'barcode'),
                      (_('Quantity'), 'quantity'),
                      (_('Price Unit'), 'price_unit'),
                      (_('Subtotal'), 'price_subtotal'),
                      ]

        col_titles = [f[0] for f in csv_fields]

        fp = io.BytesIO()
        writer = pycompat.csv_writer(fp, quoting=1)
        writer.writerow(col_titles)
        for line in self.invoice_line_ids:
            row = []
            line_values = line.get_csv_distributor_order_line_values()
            for csv_field in csv_fields:
                d = line_values[csv_field[1]]
                # Spreadsheet apps tend to detect formulas on leading =, + and -
                if isinstance(d, str) and d.startswith(('=', '-', '+')):
                    d = "'" + d

                row.append(pycompat.to_text(d))
            writer.writerow(row)

        return fp.getvalue()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    customer_id = fields.Many2one('res.partner', string='Customer')

    def unlink(self):
        for line in self:
            if line.move_id.partner_id.is_distributor and line.sale_line_ids:
                raise UserError(_("Invoice line can't be delete if a sale order and a stock move has been created. Cancel it before."))
        res = super(AccountMoveLine, self).unlink()

    def get_csv_distributor_order_line_values(self):
        vals = {'customer': self.customer_id.name,
                'street': self.customer_id.street,
                'street2': self.customer_id.street2,
                'city': self.customer_id.city,
                'zip': self.customer_id.zip,
                'country': self.customer_id.country_id.name,
                'product': self.product_id.name,
                'barcode': self.product_id.barcode,
                'quantity': self.quantity,
                'price_unit': self.price_unit,
                'price_subtotal': self.price_subtotal,
                }
        return vals

