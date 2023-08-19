window.onload = function() {

    //减少商品数量
    $('.subtract_num').click(function(){
        var num = $(this).siblings('.goods_num').val();  //得到当前兄弟文本框的值，也就是数量
        // alert(num)
        if(num<=1){
            alert("商品不可再减少了")
            num++
        }
        num--;
        //将改变后的商品数量赋值给 goods_num
        $(this).siblings('.goods_num').val(num)
        //小计
        var p =$(this).parents().siblings('.per_price').html()
        p = p.substr(1);//需要截取有用的部分：把截取￥后面的   得到单价
        $(this).parents().siblings('.sum_price').html("￥" + p*num)//单价*数量=小计  将得到的值放入‘小计’中

        getSum();
    })

    //增加商品数量
    $('.add_num').click(function(){
        var num = $(this).siblings('.goods_num').val();
        if(num>=99){
            alert("亲，我们这边没货呦！");
            num--;
        }
        num++;
        //将改变后的商品数量赋值给 goods_num
        $(this).siblings('.goods_num').val(num)

        //小计
        var p =$(this).parents().siblings('.per_price').html().substr(1)
        $(this).parents().siblings('.sum_price').html("￥" + p*num)

        getSum();
    })

    //用户修改文本框的值计算小计
    $('.goods_num').change(function() {
        // 先得到文本框的值乘以当前商品单价
        var num = $(this).val();//得到用户填入的数量
        var p =$(this).parents().siblings('.per_price').html().substr(1)
        $(this).parents().siblings('.sum_price').html("￥" + p*num)
        getSum();
    })

    //全选
    $('.checkall').change(function(){
        $('.check').prop('checked',$(this).prop('checked')) //prop表示更改标签的信息
        $('.checkall').prop('checked',$(this).prop('checked')) //两个全选按钮保持一致的chenked状态
        if ($(this).prop('checked')) {
            // 让所有商品添加check-item类名
            $('.check').addClass('check-item')
        } else {
            $('.check-item').removeClass('check-item')
        }
        getSum();
        colorChange();
    })

    //单选
    $('.check').change(function(){
        if ($(this).prop('checked')) {
            // 让选中商品添加check-item
            $(this).addClass('check-item')
        } else {
            //取消选中的去除check-item
            $(this).removeClass('check-item')
        }
        // 如果小按钮全部选中，全选按钮选中，否则不被选中
        var arrCheck = document.getElementsByClassName('check') //所有的check数量
        if($('.check-item').length == arrCheck.length){
            $('.checkall').prop('checked',true) //prop表示更改标签的信息
        }else{
            $('.checkall').prop('checked',false)
        }
        getSum();
        colorChange();
    })

    // 选中的商品那行变色
    function colorChange(){
        const check = document.querySelectorAll('.check');
        const goods = document.querySelectorAll('.goods');
        const tbody = document.querySelector('tbody');
        for(let i = 0; i < check.length; i++) {
            if (check[i].checked) {
                goods[i].style.backgroundColor="#fdf9ee"
            }else{
                goods[i].style.backgroundColor="#fff"
            }
        }
    }

    getSum();
    //全部费用  商品总数
    function getSum(){
        //将选中的商品的小计加起来
        var arrCheck = document.getElementsByClassName('check') //全部商品数组
        var arrSumNum = document.getElementsByClassName('goods_num')//全部商品对应的数量的数组
        var arrSumPrice = document.getElementsByClassName('sum_price')//全部商品对应的小计的数组
        var num=0;
        var sum=0;
        for(var i=0 ; i<arrCheck.length ;i++){
            if(arrCheck[i].checked){
                sum+=parseFloat(arrSumPrice[i].innerText.slice(1))
                num+=parseInt(arrSumNum[i].value)
            }
        }
        $('.allPrice').html("￥" +sum)
        $('.allNum').html(num)
    }

    // 删除模块
    $('.remove').click(function(){
        const check = document.querySelectorAll('.check');
        const goods = document.querySelectorAll('.goods');
        const tbody = document.querySelector('tbody');
        for(let i = 0; i < check.length; i++) {
            if (check[i].checked) {
                tbody.removeChild(goods[i]);
            }
        }
        getSum();
        $('.checkall').prop('checked',false)
    });
}
