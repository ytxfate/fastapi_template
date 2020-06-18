# fastapi_template
## flastapi 模板

### 目录说明

```
── main.py										项目启动文件
├── project										项目入口
│   ├── app.py									项目基本设置
│   ├── config									项目配置文件目录
│   │   ├── db_config.py						项目数据库连接配置文件
│   │   └── sys_config.py						项目系统配置文件
│   ├── dependencies							项目依赖
│   │   ├── auth_depend.py						Auth 认证
│   ├── endpoints								路由控制
│   │   ├── endpoints.py						路由注册
│   ├── interceptor								拦截器
│   │   ├── before_req.py						请求拦截器
│   │   ├── global_exception_handler.py			全局异常处理
│   ├── models									模型
│   │   ├── auth_models.py						Auth 认证相关模型
│   │   ├── proj_base_model.py					基本模型
│   │   └── user_models.py						用户模块相关模型
│   ├── modules									项目模块管理
│   │   ├── auth								Auth 模块
│   │   │   └── user_auth.py					Auth(登录\刷新Jwt等)
│   │   ├── info								info 模块 (scopes样例)
│   │   │   └── info.py							info 模块 (scopes样例)
│   │   └── user								user 模块开发（示例）
│   │       └── user.py							user 具体模块开发（示例）
│   └── utils									工具目录
│       ├── comm_ret.py							统一 response 封装
│       ├── handle_req_param.py					检查及处理 request 请求参数
│       ├── jwt_auth.py							JWT 编码 及 解码
│       ├── operate_minio.py					MinIO 操作（实例）
│       ├── operate_mongodb.py					MongoDB 数据库操作（实例）
│       ├── operate_redis.py					Redis 数据库操作（实例）
│       └── resp_code.py						response 状态码  （其他状态码可自行根据开发需要添加添加）									
├── requirements.txt							项目依赖
└── resources									资源目录(建议前后端分离,不使用此模块)
    ├── static									静态文件目录
    │   └── css									css 目录(示例)
    │       └── index.css						(css 文件示例)
    └── templates								html 页面目录
        └── index.html							(html 文件示例)
```



