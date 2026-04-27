from odoo import fields, models


class StudentRecord(models.Model):
    _name = "student.record"
    _description = "Student Record"

    name = fields.Char(required=True)
    age = fields.Integer()
    active = fields.Boolean(default=True)
