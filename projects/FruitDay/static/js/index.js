/**
 * Created by tarena on 18-9-6.
 */
// 网页异步检查登录状态，判断session
//　如果有信息，则显示欢迎ｘｘｘ　退出
//　如果没有信息，则显示[登录][注册有惊喜]
function checklogin() {
    $.get('/checklogin/',function (data) {
        var html = '';
        if(data.status===0){
            html+="<a href='/login'>[登录]</a>";
            html+="<a href='/register'>[注册有惊喜]</a>"
        }else if(data.status===1){
            // 用户处于登录状态
            user = JSON.parse(data.user);
            // console.log(user);
            html+="欢迎："+user.uname+"&nbsp;&nbsp;";
            html+="<a href='/logout'>退出</a>"
        }
        $("#list>li:first").html(html)
    },'json')
}

function loadgoods() {
    $.ajax({
        url:"/loadgoods/",
        type:'get',
        // data:null,
        dataType:'json',
        success:function (data) {
            var html = '';
            //　循环遍历json对象
            $.each(data,function (i,obj) {
                html+="<div class='item'>";
                var typeobj = JSON.parse(obj.type);
                html+="<p class='title'>";
                    html+="<a href='#'>更多</a>";
                    html+="<img src='/"+typeobj.picture+"'>";
                html+="</p>";
                html+="<ul>";
                    // 将obj.goods转换成json数组
                    var goodsarr = JSON.parse(obj.goods);
                    // 遍历类别中每一个商品
                    $.each(goodsarr,function (i,goods) {
                        // console.log(goods);
                        html+="<li ";
                        if((i+1)%5===0)
                            html+="class='no-margin'";
                        html+=">";
                            html+="<p>";
                                html+="<img src='/"+goods.fields.picture+"'>";
                            html+="</p>";
                            html+="<div class='content'>";
                                html+="<a href='javascript:add_cart("+goods.pk+")' class='cart'>";
                                    html+="<img src='/static/images/cart.png'>";
                                html+="</a>";
                                html+="<p>"+goods.fields.title+"</p>";
                                html+="<span>&yen"+goods.fields.price+"/"+goods.fields.spec+"</span>";
                            html+="</div>";
                        html+="</li>"
                    });
                html+="</ul>";
                html+="</div>"
            });
            $("#main").html(html)
        },
        async:true
    })
}

function add_cart(goods_id) {
    //　检查用户的登录状态
    $.get('/checklogin/',function (data) {
        if(data.status===0){
            alert("请先登录")
        }else {
            $.get('/add_cart/','goods_id='+goods_id,function (data) {
                console.log(data);
                if(data.status===1){
                    alert(data.text);
                    loadcount()
                }else{
                    alert(data.text)
                }
            },'json')
        }
    },'json')
}

// 加载当前用户购物车商品数量
function loadcount() {
    $.get('/cart_count/',function (data) {
        $("#myCart>a").html("我的购物车（"+data.count+"）");
    },'json')
}


$(function () {
   checklogin();
    loadgoods();
    loadcount()
});