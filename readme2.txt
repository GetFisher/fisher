==================
项目：fruitday

任务1：
	1.创建数据库-FruitDay
	2.在FruitDay项目中完成数据的配置
	3.同步基础设置到数据库中
任务2：
	1.创建Models-Users
	2.包含以下字段
		1.手机号 - uphone，max_length 20
		2.密码 - upwd，max_length 20
		3.电子邮箱 - uemali
		4.用户名 - uname max_length20
		5.是否激活 - isActive，布尔类型，默认为True
	3.同步回数据库
任务3：注册前的数据验证（失去焦点）
	1.手机号：
		1.不能为空
		2.号码格式（可选，使用正则）
		3.验证时候存在
		给出提示 通过/错误内容
	2.密码
		1.6位以上
	3.确认密码
		1.必须与密码一致
	4.用户名
		1.不能为空
	5.邮箱
		1.不能为空
		2.格式（可选，正则）
任务：
	首页的登录信息显示
	1.如果没有用户东路，显示[登录][注册有惊喜]
	2.如果已经登录的话，显示  欢迎：xxx 退出（超链接）
	3.使用AJAX判断登录信息
		网页加载时就判断是否有登录信息
	4.推荐步骤
		1.判断session 中是否有登录信息
		2.退出，清除session中的登录信息，清除cookie中的登录信息
			resp.delete_cookie('key')
NEXT
	1.创建商品类型的Models
		表1名称GoodsType
			字段：
				1.title - 商品类型的名称
				2.picture - 指定商品的图片
					models.ImageField（upload_to="static/upload/goodstype"）
				3.desc - 商品类型的描述
		表2.商品Goods：
			字段：
				1.title - 商品的名称
				2.price - 商品价格
				3.spec - 商品规格（描述单位）
				4.picture - 商品图片
					models.ImageField（upload_to="static/upload/goods"）
				5.goodsType - 商品类型
					引用自GoodsType实体
				6.isActive是否上架
					models.BooleanField()
mission3
	按照数据的存储按照商品的类别进行商品的加载
		1.使用AJAX向服务器发送请求，并接收数据
		（类别及类别下的商品）
		2.在前端中对数据进行解析，按照HTML规定的格式进行显示
