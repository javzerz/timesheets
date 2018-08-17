$(document).ready( function () {
    $('#it').DataTable({
      paging:false,
      searching:false,
      "scrollX": true
    });
} );

$('#myModal').on('shown.bs.modal', function () {
})

$(".nav .nav-link").on("click", function(){
   $(".nav-link").find(".active").removeClass("active");
   $(this).addClass("active");
});
