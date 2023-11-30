from odoo import SUPERUSER_ID, api

# For details, see https://alfatech2020.atlassian.net/browse/OD-919


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    modules = env["ir.module.module"].search(
        [
            (
                "name",
                "in",
                (
                    "documents",
                    "web_grid",
                    "web_gantt",
                    "web_enterprise",
                    "web_map",
                    "spreadsheet_edition",
                    "web_cohort",
                ),
            )
        ]
    )
    modules.write({"state": "installed"})
    for module in modules:
        module.button_uninstall()
