from openerp import models, fields, api

class Wizard(models.TransientModel):

    _name = 'openacademy.wizard'


    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session',string='Sessions',
                                   default= _default_sessions, required=True)
    participant_ids = fields.Many2many('res.partner',string='Participants')

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.participant_ids |= self.participant_ids
        return {}