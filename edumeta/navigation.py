"""
Central navigation registry for the tenant-facing UI.
Each item is filtered by role in the context processor.
"""

NAV_ITEMS = [
    {
        "label": "Dashboard",
        "url_name": "dashboard",
        "section": "dashboard",
        "icon": "dashboard",
        "roles": ("admin", "teacher", "student", "parent"),
    },
    {
        "label": "Academics",
        "url_name": "academics:index",
        "section": "academics",
        "icon": "academics",
        "roles": ("admin", "teacher", "student", "parent"),
        "children": [
            {"label": "Overview", "url_name": "academics:index", "roles": ("admin", "teacher", "student", "parent")},
            {"label": "Sessions & terms", "url_name": "academics:sessions", "roles": ("admin", "teacher")},
            {"label": "Classes & subjects", "url_name": "academics:classes", "roles": ("admin", "teacher")},
            {"label": "Reports & grades", "url_name": "academics:reports", "roles": ("admin", "teacher", "student", "parent")},
        ],
    },
    {
        "label": "People",
        "url_name": "people:index",
        "section": "people",
        "icon": "people",
        "roles": ("admin", "teacher", "student", "parent"),
        "children": [
            {"label": "Overview", "url_name": "people:index", "roles": ("admin", "teacher", "student", "parent")},
            {"label": "Students", "url_name": "people:students", "roles": ("admin", "teacher", "student", "parent")},
            {"label": "Teachers", "url_name": "people:teachers", "roles": ("admin",)},
            {"label": "Parents", "url_name": "people:parents", "roles": ("admin", "teacher")},
        ],
    },
    {
        "label": "Attendance",
        "url_name": "attendance:index",
        "section": "attendance",
        "icon": "attendance",
        "roles": ("admin", "teacher", "student", "parent"),
    },
    {
        "label": "Finance",
        "url_name": "finance:index",
        "section": "finance",
        "icon": "finance",
        "roles": ("admin", "parent"),
    },
]
