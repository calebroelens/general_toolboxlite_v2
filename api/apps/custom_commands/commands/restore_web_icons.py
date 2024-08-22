from abc import ABC
from core.odoo.client import OdooClient
from api.apps.custom_commands.commands import BaseCommand
import json


class RestoreWebIcons(BaseCommand):

    title = "Restore icons"
    desc = "Restore the application icons"
    technical_name = "restore_web_icons"

    @staticmethod
    def run(client: OdooClient):
        menu_items = client.execute_kw_models(
            'ir.ui.menu',
            'search_read',
            [[['active', '=', True], ['web_icon', '!=', False]]],
            {'fields': ['id', 'web_icon']}
        )
        for index, menu_item in enumerate(menu_items):
            icon = menu_item['web_icon']
            client.execute_kw_models(
                'ir.ui.menu',
                'write',
                [[menu_item['id']], {'web_icon': icon}],
                {}
            )
            status = {"status": f"Restoring icons {index+1}/{len(menu_items)}", "progress": index+1, "max": len(menu_items)}
            yield f"event: custom_command\ndata:{json.dumps(status)}\n\n"



