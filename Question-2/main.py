"""
Question 2:
Create a Python script that implements the following tasks:
Task 2a: Model Definition
Task 2b: Views Definition
Task 2c: Menu + Action
Task 2d: Button method to deactivate student
Task 2e: View Inheritance
"""

# =========================
# Task 2a: Model Definition
# =========================

from odoo import fields, models


class StudentRecord(models.Model):
    _name = "student.record"
    _description = "Student Record"

    name = fields.Char(required=True)
    age = fields.Integer()
    active = fields.Boolean(default=True)

    # Task 2d: Button method to deactivate student.
    def action_deactivate_student(self):
        self.write({"active": False})


# =========================
# Task 2b: Views Definition
# =========================
# Put this XML content in your module's views XML file (e.g., views/student_record_views.xml)

TASK_2B_VIEWS_XML = """
<odoo>
    <record id="view_student_record_tree" model="ir.ui.view">
        <field name="name">student.record.tree</field>
        <field name="model">student.record</field>
        <field name="arch" type="xml">
            <tree string="Student Records">
                <field name="name"/>
                <field name="age"/>
                <field name="active"/>
            </tree>
        </field>
    </record>

    <record id="view_student_record_form" model="ir.ui.view">
        <field name="name">student.record.form</field>
        <field name="model">student.record</field>
        <field name="arch" type="xml">
            <form string="Student Record">
                <header>
                    <button
                        name="action_deactivate_student"
                        string="Deactivate Student"
                        type="object"
                        class="btn-primary"
                    />
                </header>
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="age"/>
                        <field name="active"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
""".strip()


# =========================
# Task 2c: Menu + Action
# =========================
# The Students submenu opens student records in tree/form mode.

TASK_2C_MENU_XML = """
<odoo>
    <record id="action_student_record" model="ir.actions.act_window">
        <field name="name">Students</field>
        <field name="res_model">student.record</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_school_root" name="School" sequence="10"/>
    <menuitem
        id="menu_school_students"
        name="Students"
        parent="menu_school_root"
        action="action_student_record"
        sequence="20"
    />
</odoo>
""".strip()


# =========================
# Task 2e: View Inheritance
# =========================
# Hide age field on form view using xpath.

TASK_2E_INHERIT_XML = """
<odoo>
    <record id="view_student_record_form_hide_age" model="ir.ui.view">
        <field name="name">student.record.form.hide.age</field>
        <field name="model">student.record</field>
        <field name="inherit_id" ref="view_student_record_form"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='age']" position="attributes">
                <attribute name="invisible">1</attribute>
            </xpath>
        </field>
    </record>
</odoo>
""".strip()
