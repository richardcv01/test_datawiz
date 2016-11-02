    // Магія розпочнеться лише після повного завантаження сторінки
    $(document).ready(function (){

        $("#selplus").change(function() {
            var selplus = $("#selplus").val();
            // AJAX-запит на потрібну адресу
            $.get("/client/table/",{col:selplus, znak:'plus'}, function(data){
               $('#ltable').html(data);

            });
        });
        $("#selminus").change(function() {
           var  selminus = $("#selminus").val();
            // AJAX-запит на потрібну адресу
            $.get("/client/table/",{col:selminus, znak:'minus'}, function(data){
               $('#rtable').html(data);

            });
        });
    });


