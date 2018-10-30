/**
 * Created by tarena on 18-9-5.
 */
// 功能：验证手机号码
// 返回值：
//　true:通过验证
//　false:未通过验证
function checkuphone() {
    var value = $("[name='uphone']").val();
    // 在window顶层变量中增加flag,默认值为false
    window.flag=false;
    // 去掉两端的空格后再验证长度
    if(value.trim().length===11){
        // 格式通过，验证手机号码是否存在

        $.ajax({
            url:"/checkuphone/",
            type:"post",
            // data:"uphone="+value   //参数较少使用此方法拼接，较多则采用json格式，如下
            data:{
                uphone:value,
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
            },
            dataType:'json',
            async:false,
            success:function (data) {
                //data 为服务器响应的数据
                $("#uphone-show").html(data.text);
                if(data.status === 1){
                    //　注意函数的作作用域
                    window.flag=true;
                    // console.log('1')
                    }
                else{
                    window.flag=false;
                    // console.log('2')
            }}
        })
    }else{
        $("#uphone-show").html('手机号码位数不对');
        return false;
    }
    return window.flag
}

//　验证密码
function checkupwd() {
    // 检查密码是否规范
    // 返回值
    var upwd = $("[name='upwd']").val();
    if(upwd.length>=6){
        $("#upwd-show").html("通过");
        return true
    }
    $("#upwd-show").html("密码不符合要求");
    return false
}
// ＤＯＭ树加载完成时要执行的操作，初始化操作，如事件的绑定
$(function () {
    // 为name=uphone的元素绑定blur时间
    $("[name='uphone']").blur(function () {
        checkuphone();
    });
    // 为密码验证函数绑定blur事件
    $("[name='upwd']").blur(function () {
        checkupwd()
    });
    // bababa...
    // 为from绑定提交事件submit,调用验证所有记录，用&&连接
    $("#frmregister").submit(function () {
        return checkupwd()&&checkuphone()
    })
});