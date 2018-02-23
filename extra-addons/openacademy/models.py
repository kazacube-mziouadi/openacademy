# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, exceptions, _

class Course(models.Model):
    _name = 'openacademy.course'

    title = fields.Char(string='Titre',required=True)

    _rec_name = 'title'
    description = fields.Text(string='Description')
    responsable_id = fields.Many2one('res.users',ondelete='set null', string='Responsable',index=True)
    session_ids = fields.One2many('openacademy.session','cour_id', string='Sessions')



    _sql_constraints = [
        (
            'title_description_verif',
            'CHECK(title != description)',
            'Le titre du cour doit être différent de la description'
        ),
        (
            'title_unique',
            'UNIQUE(title)',
            'Le titlre du cour êxistant'
        )
    ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('title','=like',_(u"Copy of {}%").format(self.title))]
        )
        if not copied_count:
            new_name = _(u'Copy of {}').format(self.title)
        else:
            new_name = _(u'Copy of {} ({})').format(self.title, copied_count)
        default['title'] = new_name
        return super(Course, self).copy(default)

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(string='Nom',required=True)
    date_debut = fields.Date(string='Date Début',default=fields.Date.today)
    date_fin = fields.Date(string="Date Fin", store=True, compute="_get_date_fin",inverse='_set_date_fin')
    duree = fields.Float(digits=(6, 2),help='Durée pour un jour')
    nbr_place = fields.Integer(string='Nombre de Place')
    instructeur_id = fields.Many2one('res.partner',string='Instructeur',
                                     domain=[('instructeur','=',True)])
    cour_id = fields.Many2one('openacademy.course',ondelete='cascade',string='Cour',required=True)

    participant_ids = fields.Many2many('res.partner', string='Participants')
    active = fields.Boolean(default=True)
    place_occupe = fields.Float(string='Places Occupées', compute='_place_occup')

    heures = fields.Float(string='Durée en Heure',compute='_get_heures', inverse='_set_heures')

    nbr_participants = fields.Integer(string='Nombre de Participants',
                                      compute='_get_nbr_participants', store=True)
    color = fields.Integer()

    state = fields.Selection([
        ('brouillon', "Brouillon"),
        ('confirme', "Confirme"),
        ('termine', "Termine"),
    ], default='brouillon')

    @api.multi
    def action_brouillon(self):
        self.state = 'brouillon'

    @api.multi
    def action_confirm(self):
        self.state = 'confirme'

    @api.multi
    def action_termine(self):
        self.state = 'termine'

    @api.depends('participant_ids')
    def _get_nbr_participants(self):
        for r in self:
            r.nbr_participants = len(r.participant_ids)

    @api.depends('duree')
    def _get_heures(self):
        for r in self:
            r.heures = r.duree * 24

    def _set_heures(self):
        for r in self:
            r.duree = r.heures / 24

    @api.depends('duree','date_debut')
    def _get_date_fin(self):
        for r in self:
            if not (r.date_debut and r.duree):
                r.date_fin = r.date_debut
                continue

            debut = fields.Datetime.from_string(r.date_debut)
            dure = timedelta(days=r.duree, seconds=-1)
            r.date_fin = debut + dure

    def _set_date_fin(self):
        for r in self:
            if not (r.date_debut and r.date_fin):
                continue

            date_debut = fields.Datetime.from_string(r.date_debut)
            date_fin = fields.Datetime.from_string(r.date_fin)
            r.duree = (date_fin - date_debut).days + 1

    @api.depends('participant_ids','nbr_place')
    def _place_occup(self):
        for r in self:
            if not r.nbr_place:
                r.place_occupe = 0.0
            else:
                r.place_occupe = 100 * len(r.participant_ids) / r.nbr_place

    @api.constrains('nbr_place','participant_ids')
    def verif_valid_place(self):
        if self.nbr_place < 0:
            raise exceptions.ValidationError(_("Le nombre de place ne peut pas être négative"))
        if self.nbr_place < len(self.participant_ids):
            raise exceptions.ValidationError(_("Les places de la sessions sont réservées"))

    @api.constrains('participant_ids','instructeur_id')
    def _verif_instr_particip(self):
        for r in self:
            if r.instructeur_id in r.participant_ids:
                raise exceptions.ValidationError(_("l'instructeur de la session ne peut pas être particpant"))