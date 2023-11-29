$(".o_close_btn").on("click", function () {
  $(".o_viewer_pdf").remove();
  $(".pdf_preview").hide();
});

$(".preview_icon").on("click", function () {
  let dataUrl = $(this).attr("data-url");
  let viewerType = $(this).attr("data-viewer-type");
  let srcUrl = "";

  switch (viewerType) {
    case "office.live":
      srcUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${dataUrl}`;
      break;
    case "pdfjs":
      srcUrl = `/web/static/lib/pdfjs/web/viewer.html?file=${dataUrl}`;
      break;
    default:
      // unsupported viewer type, modal window must be closed and container removed from DOM
      $(".o_viewer_pdf").remove();
      $(".pdf_preview").hide();
      return;
  }

  let iframe = $(`<iframe class="mt32 o_viewer_pdf" src="${srcUrl}" />`);

  $(".o_viewer_zoomer").append(iframe);
  $(".pdf_preview").show();
});
