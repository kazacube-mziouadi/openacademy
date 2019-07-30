from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    instructeur = fields.Boolean("Instructeur",default=False)

    session_ids = fields.Many2many('openacademy.session',
                                   string='Sessions Participes',readonly=True)
