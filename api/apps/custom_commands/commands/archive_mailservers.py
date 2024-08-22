from abc import ABC

from core.odoo.client import OdooClient
from api.apps.custom_commands.commands import BaseCommand
import json


class ArchiveMailServers(BaseCommand):

    title = "Archive outgoing mail servers"
    desc = "Archive outgoing mail servers. Model ir.mail_server"
    technical_name = "archive_outgoing_mail_servers"

    @staticmethod
    def run(client: OdooClient):
        mail_servers = client.execute_kw_models(
            'ir.mail_server',
            'search',
            [[]],
            {}
        )
        if mail_servers:
            client.execute_kw_models(
                'ir.mail_server',
                'write',
                [mail_servers, {'active': False}],
                {}
            )
        status = {"status": f"Archived {len(mail_servers)} outgoing mail servers.", "progress": 100, "max": 1}
        yield f"event: custom_command\ndata:{json.dumps(status)}\n\n"


