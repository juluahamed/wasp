function validateForm() {
    var cName = document.forms["newcategoryForm"]["catName"].value;
    if (cName == "") {
        $('.new-category-alert').css("display", "block");
        return false;
    }
    
}
$(document).ready(function(){
	$(".box_grid").click(function(){
		window.location.href = $(this).attr("redir");
	});
});



