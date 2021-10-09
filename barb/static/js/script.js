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
    pesq = ''
    $('#search').bind('keyup', function(event){
        
        _filterObj = $(".filter-checkbox").serialize();
        
        
        // console.log(pesq,'  ',$(this).val())
        if (pesq != $(this).val()){
            pesq = $(this).val()
            $.ajax({
                url:"/prods",
                data:_filterObj+'&search='+pesq,
                /*dataType:'json',*/
                beforeSend:function(){
                    $(".ajaxLoader").show()
                },
                success:function(res){
                    $("#filteredProducts").html(res)
                    $(".ajaxLoader").hide()
                }
            })
        }else{
            console.log(pesq)
        }
        
    })
    $(".filter-checkbox").on('click', function(){
        var _filterObj;
        
        pesq = $('#search').val()
        _filterObj = $(".filter-checkbox").serialize();
        // alert(_filterObj)
        $.ajax({
            url:"/prods",
            data:_filterObj+'&search='+pesq,
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

    var qntInput = $('.qty')
    var qntPlus = $('.plus')
    var qntMin = $('.minus')
    
    var qntAct = {}


    
    pesq = ''
    $('#search').bind('keyup', function(event){
        
        _filterObj = $(".filter-checkbox").serialize();
        
        
        // console.log(pesq,'  ',$(this).val())
        if (pesq != $(this).val()){
            pesq = $(this).val()
            $.ajax({
                url:"/prods",
                data:_filterObj+'&search='+pesq,
                /*dataType:'json',*/
                beforeSend:function(){
                    $(".ajaxLoader").show()
                },
                success:function(res){
                    $("#filteredProducts").html(res)
                    $(".ajaxLoader").hide()
                }
            })
        }
    })
    
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
                success:function(res){
                    $('.'+a).find('#total-prod-item').text(res.data)
                    
                }
            })
        })
    })


});