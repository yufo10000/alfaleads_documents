odoo.define(
  "alfaleads_documents/static/src/js/alfaleads_documents_search_panel_model_extension",
  function (require) {
    "use strict";

    const DocumentsSearchPanelModelExtension = require("documents/static/src/js/documents_search_panel_model_extension");

    function _getCategoryDomain(excludedCategoryId) {
      const domain = [];
      for (const category of this.categories) {
        if (category.id === excludedCategoryId || !category.activeValueId) {
          continue;
        }
        const field = this.config.fields[category.fieldName];
        const operator =
          field.type === "many2one" &&
          category.parentField &&
          category.fieldName !== "folder_id"
            ? "child_of"
            : "=";
        domain.push([category.fieldName, operator, category.activeValueId]);
      }
      return domain;
    }

    DocumentsSearchPanelModelExtension.prototype._getCategoryDomain = _getCategoryDomain;

    return DocumentsSearchPanelModelExtension;
  }
);
