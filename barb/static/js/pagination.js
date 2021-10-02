$(document).ready(function () {

    
    $(".page-link").on('click', function(e){
        e.preventDefault();
        _filterObj = $(".filter-checkbox").serialize();
        page = $(this).attr('href')
        pesq = $('#search').val()
        $.ajax({
            url:"/prods",
            data:_filterObj+'&page='+page+'&search='+pesq,
            /*dataType:'json',*/
            beforeSend:function(){
                $(".ajaxLoader").show()
            },
            success:function(res){
                $("#filteredProducts").html(res)
                $(".ajaxLoader").hide()
            }
        })
    })
})