$(document).ready(function () {
    // var baseUrl = 'http://127.0.0.1:8000/' 
    var $campo = $("#id_cep");
    
    var searchBtn = $('#search-btn')
    var searchForm = $('#search-form')

    $(searchBtn).on('click', function(){
        searchForm.submit();
    })
    $campo.mask('00000-000', {reverse: true});
    
    $(".ajaxLoader").hide()
    

    $(".filter-checkbox").on('click', function(){
        var _filterObj;
        _filterObj = $(".filter-checkbox").serialize();

        $.ajax({
            url:"/prods",
            data:_filterObj,
            /*dataType:'json',*/
            beforeSend:function(){
                $(".ajaxLoader").show()
            },
            success:function(res){
                $("#filteredProducts").html(res)
                $(".ajaxLoader").hide()
                window.scrollTo(0, 10)
            }
        })
    })

    var qntInput = $('.qty')
    var qntPlus = $('.plus')
    var qntMin = $('.minus')
    
    var qntAct = {}


    

    $(qntPlus).each(function(i) {
        $(this).on("click",function(){
            a = $(this).data('name')
            qntAct[a] = parseFloat($('input[id='+$(this).attr("for")+']').val()) + 1
            // alert($(this).data('name'))
            if (qntAct[a] > 10){
                qntAct[a] = 10
                $('input[id='+$(this).attr("for")+']').val(10)
            }else{
                $('input[id='+$(this).attr("for")+']').val(qntAct[a])
            }
             
            qntAct['click'] = a
            console.log(qntAct)
            $.ajax({
                url:"/cart",
                data:qntAct,
                dataType:'json',
                beforeSend:function(){
                    console.log("error")
                },
                success:function(res){
                    $('.'+a).find('#total-prod-item').text(res.data)
                }
            })
        })
    })
    
    $(qntMin).each(function(i) {
        $(this).on("click",function(){
            a = $(this).data('name')
            qntAct[a] =  parseFloat($('input[id='+$(this).attr("for")+']').val()) - 1
            if (qntAct[a] < 1){
                qntAct[a] = 1
                $('input[id='+$(this).attr("for")+']').val(1)
            }else{
                $('input[id='+$(this).attr("for")+']').val(qntAct[a])
            }
            qntAct['click'] = a

            $.ajax({
                url:"/cart",
                data:qntAct,
                dataType:'json',
                beforeSend:function(){
                    console.log('error')
                },
                success:function(res){
                    $('.'+a).find('#total-prod-item').text(res.data)
                    
                }
            })
        })
    })


});