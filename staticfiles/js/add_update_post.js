
$(document).ready(function () {
  // Prepare the preview for profile picture
  $("#id_header_image").change(function () {
    readURL(this);
  });
});

$(document).ready(function () {
  // Prepare the preview for profile picture
  $("#id_picture").change(function () {
    readURL(this);
  });
});

$(document).ready(function () {
  // Prepare the preview for profile picture
  $("#id_avatar").change(function () {
    readURL(this);
  });
});

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#wizardPicturePreview").attr("src", e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}
$("pre").wrapInner('<code class="language-python"></code>');

$(".selectmultiple").attr({
  "data-max-options": "3",
  "data-live-search": true,
  "data-width": "fit",
  "data-style": "btn-outline-info",
  title: "Select categories...",
  "data-selected-text-format": "count > 3",
});
$("select").selectpicker();
