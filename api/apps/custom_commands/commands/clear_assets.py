from core.odoo.client import OdooClient
from api.apps.custom_commands.commands import BaseCommand
import json


class ClearAssets(BaseCommand):

    technical_name = "clear_assets"
    title = "Clear Assets (JS/CSS)"
    desc = "Clear JS & CSS assets. ([|, [name, ilike, %.js%], [name, ilike, %.css%]])"

    @staticmethod
    def run(client: OdooClient):
        assets = client.execute_kw_models(
            'ir.attachment',
            'search',
            [['|', ['name', 'ilike', '%.js%'],
             ['name', 'ilike', '%.css%']]],
            {}
        )
        if assets:
            for index, asset in enumerate(assets):
                client.execute_kw_models(
                    'ir.attachment',
                    'unlink',
                    [[asset]],
                    {}
                )
                status = {"status": f"Removing assets... {index+1}/{len(assets)}", "progress": index + 1, "max": len(assets)}
                yield f"event: custom_command\ndata:{json.dumps(status)}\n\n"

