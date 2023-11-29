odoo.define("alfaleads_documents.DocumentsInspector", function (require) {
  "use strict";

  const { _t, qweb } = require("web.core");
  const DocumentsInspector = require("documents.DocumentsInspector");

  DocumentsInspector.include({
    events: {
      "click .o_inspector_contract_name": "_onOpenContract",
      "click .o_inspector_archive": "_onArchive",
      "click .o_inspector_request_icon": "_onClickRequestIcon",
      "click .o_inspector_delete": "_onDelete",
      "click .o_inspector_download": "_onDownload",
      "click .o_inspector_replace": "_onReplace",
      "click .o_inspector_split": "_onClickSplit",
      "click .o_inspector_history_item_delete": "_onClickHistoryItemDelete",
      "click .o_inspector_history_item_download": "_onClickHistoryItemDownload",
      "click .o_inspector_history_item_restore": "_onClickHistoryItemRestore",
      "click .o_inspector_lock": "_onLock",
      "click .o_inspector_share": "_onShare",
      "click .o_inspector_open_chatter": "_onOpenChatter",
      "click .o_inspector_tag_add": "_onTagInputClicked",
      "click .o_inspector_tag_remove": "_onRemoveTag",
      "click .o_inspector_trigger_rule": "_onTriggerRule",
      "click .o_inspector_object_name": "_onOpenResource",
      "click .o_preview_available": "_onOpenPreview",
      "click .o_document_pdf": "_onOpenPDF",
      "mouseover .o_inspector_trigger_hover": "_onMouseoverRule",
      "mouseout .o_inspector_trigger_hover": "_onMouseoutRule",
    },
    _renderFields: function () {
      const options = { mode: "edit" };
      const proms = [];
      if (this.records.length === 1) {
        proms.push(this._renderField("name", options));
        if (this.records[0].data.type === "url") {
          proms.push(this._renderField("url", options));
        }
      }
      if (this.records.length > 0) {
        proms.push(this._renderField("owner_id", options));
        proms.push(
          this._renderField("folder_id", {
            icon: "fa fa-folder o_documents_folder_color",
            mode: "edit",
          })
        );
      }
      return Promise.all(proms);
    },
    _renderModel: function () {
      this._super(...arguments);
      if (this.records.length !== 1) {
        return;
      }
      const $modelContainer = this.$(".o_model_container");
      const record = this.records[0];

      if (
        [
          "alfaleads_documents.appendix",
          "alfaleads_documents.add_agreement",
          "alfaleads_documents.accounting_document",
        ].includes(record.data.res_model) &&
        record.data.contract_id
      ) {
        const contract_options = {
          res_model: "alfaleads_documents.contract",
          res_name: record.data.contract_id.data.display_name,
        };
        $modelContainer.after(
          qweb.render(
            "alfaleads_documents.DocumentsInspector.relatedContract",
            contract_options
          )
        );
      }
    },
    _onOpenContract: function () {
      const record = this.records[0];
      this.trigger_up("open_record", {
        resId: record.data.contract_id.res_id,
        resModel: record.data.contract_id.model,
      });
    },
  });
});
