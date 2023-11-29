/** @odoo-module **/

import { registry } from "@web/core/registry";

import { DocumentsListView } from "@documents/views/list/documents_list_view";
import { DocumentsListController } from "@documents/views/list/documents_list_controller";

export class AlfaleadsDocumentsListController extends DocumentsListController {
  setup() {
    super.setup();
    Object.assign(this, {
      hasDisabledButtons: () => {
        const folder = this.env.searchModel.getSelectedFolder();
        return (
          Boolean(this.props.context.document_model) ||
          !folder.id ||
          !folder.has_write_access
        );
      },

      hasShareDocuments: () => {
        const folder = this.env.searchModel.getSelectedFolder();
        return Boolean(this.props.context.document_model) || !folder.id;
      },
    });
  }

  get visibleCreateDocument() {
    return (
      this.props.context.document_model &&
      this.env.searchModel.getSelectedFolderId()
    );
  }

  onClickCreateFolder() {
    this._createObject(
      "documents.folder",
      {
        default_parent_folder_id: this.env.searchModel.getSelectedFolderId(),
      },
      "new"
    );
  }

  onClickCreateDocument() {
    let modelName = this.props.context.document_model;
    if (!modelName) return;

    this._createObject(
      modelName,
      {
        default_folder_id: this.env.searchModel.getSelectedFolderId(),
      },
      "current"
    );
  }

  _createObject(modelName, context, target = "current") {
    console.error(this);
    this.action.doAction({
      type: "ir.actions.act_window",
      res_model: modelName,
      views: [[false, "form"]],
      target: target,
      context: context,
    });
  }
}

registry.category("views").add("alfaleads_documents_list_js", {
  ...DocumentsListView,
  Controller: AlfaleadsDocumentsListController,
});
