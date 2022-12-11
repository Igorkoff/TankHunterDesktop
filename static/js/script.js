/* Preview of an Image */

$(document).on("click", ".browse", function() {
  let file = $(this).parents().find(".file");
  file.trigger("click");
});

$('input[type="file"]').change(function(e) {
  let fileName = e.target.files[0].name;
  $("#id_file").val(fileName);

  let reader = new FileReader();
  reader.onload = function(e) {
    document.getElementById("preview").src = e.target.result;
  };

  reader.readAsDataURL(this.files[0]);
});


/* Leaflet JS */

