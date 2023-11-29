odoo.define("alfaleads_documents.MsDocsDocumentViewer", function (require) {
  "use strict";

  const DocumentViewer = require("documents.DocumentViewer");

  DocumentViewer.include({
    async start() {
      await this._super(...arguments);
      const isMsOnly = this._documents.every(
        (record) => record.viewer_type === "office.live"
      );
      if (isMsOnly | (this.activeAttachment.viewer_type === "office.live")) {
        await this._renderMS(this._documents);
      }
    },

    async _renderMS(documents) {
      const doc = documents[0];
      const $documentViewerElements = this.$(".move_previous, .move_next");
      $documentViewerElements.addClass("o_hidden");
      this._rpc({
        model: "documents.document",
        method: "share_for_preview",
        args: [doc.id, doc.folder_id.data.id],
      }).then(
        (result) => {
          const srcUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${result}`;
          const iframe = $(
            `<iframe class="mt32 o_viewer_pdf" src="${srcUrl}" />`
          );
          $(".o_viewer_zoomer").append(iframe);
        },
        (error) => {
          this.destroy();
        }
      );
    },
  });
});
