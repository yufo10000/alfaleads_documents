import logging

from odoo import http
from odoo.addons.documents.controllers.main import ShareRoute
from odoo.http import request

logger = logging.getLogger(__name__)


class RestrictedShareRoute(ShareRoute):
    @http.route(
        ["/document/tmp_preview/<int:share_id>/<access_token>/<int:id>"],
        type="http",
        auth="public",
    )
    def download_and_kill_share(
        self, id=None, access_token=None, share_id=None, **kwargs
    ):
        try:
            document = self._get_file_response(
                id, share_id=share_id, share_token=access_token, field="datas"
            )
            if document:
                request.env["documents.share"].sudo().browse(int(share_id)).unlink()
                return document
            else:
                return request.not_found()
        except Exception:
            logger.exception("Failed to download document %s" % id)

        return request.not_found()
