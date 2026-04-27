{
    "name": "School Management",
    "summary": "Student records management",
    "version": "1.0.0",
    "category": "Education",
    "author": "Interview Candidate",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/student_record_views.xml",
        "views/student_record_menu.xml",
        "views/student_record_button.xml",
        "views/student_record_hide_age.xml",
    ],
    "installable": True,
    "application": True,
}
