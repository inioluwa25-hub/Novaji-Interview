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
