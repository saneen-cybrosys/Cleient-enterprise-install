# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class User(models.Model):
    _inherit = ['res.users']

    next_appraisal_date = fields.Date(related='employee_id.next_appraisal_date')
    last_appraisal_date = fields.Date(related='employee_id.last_appraisal_date')
    last_appraisal_id = fields.Many2one(related='employee_id.last_appraisal_id')

    def get_employee_autocomplete_ids(self):
        self.ensure_one()
        if self.user_has_groups('hr_appraisal.group_hr_appraisal_user'):
            return self.env['hr.employee'].search([('company_id', 'in', self.env.companies.ids)])
        user_employees = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        children = self.env['hr.employee'].search([
            ('id', 'child_of', user_employees.ids),
            ('company_id', 'in', self.env.companies.ids),
        ])
        return children | self.env.user.employee_ids

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            'next_appraisal_date',
            'last_appraisal_date',
            'last_appraisal_id',
        ]

    def action_send_appraisal_request(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.appraisal',
            'name': 'Appraisal Request',
            'context': self.env.context,
        }

    def action_open_last_appraisal(self):
        self.ensure_one()
        return {
            'view_mode': 'form',
            'res_model': 'hr.appraisal',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.last_appraisal_id.id,
        }
