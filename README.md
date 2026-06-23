# fastapi_template
## flastapi 模板

### 目录说明

```
📦fastapi_template
 ┣ 📂project
 ┃ ┣ 📂config                                    配置
 ┃ ┃ ┣ 📜api_json.py                            接口文档
 ┃ ┃ ┣ 📜db_config.py                           数据库配置
 ┃ ┃ ┣ 📜logging.prod.ini                       生产日志配置
 ┃ ┃ ┣ 📜logging.test.ini                       测试日志配置
 ┃ ┃ ┗ 📜sys_config.py                          系统配置
 ┃ ┣ 📂dependencies                              依赖
 ┃ ┃ ┣ 📜auth_depend.py                         认证
 ┃ ┃ ┗ 📜download_depend.py                     下载认证
 ┃ ┣ 📂endpoints                                路由控制
 ┃ ┃ ┗ 📜endpoints.py                           路由注册
 ┃ ┣ 📂interceptor                              拦截器
 ┃ ┃ ┣ 📜before_req.py                          请求拦截器
 ┃ ┃ ┗ 📜global_exception_handler.py            全局异常处理
 ┃ ┣ 📂models                                   模型
 ┃ ┃ ┣ 📜auth_models.py                         Auth 认证相关模型
 ┃ ┃ ┣ 📜com_validator.py                       公共默认验证器
 ┃ ┃ ┣ 📜proj_base_model.py                     基本模型
 ┃ ┃ ┗ 📜user_models.py                         用户模块相关模型
 ┃ ┣ 📂modules                                  项目模块管理
 ┃ ┃ ┣ 📂auth                                   Auth 模块
 ┃ ┃ ┃ ┗ 📜user_auth.py                         Auth(登录\刷新Jwt等)
 ┃ ┃ ┣ 📂info                                   info 模块 (scopes样例)
 ┃ ┃ ┃ ┗ 📜info.py                              info 模块 (scopes样例)
 ┃ ┃ ┗ 📂user                                   user 模块开发（示例）
 ┃ ┃ ┃ ┗ 📜user.py                              user 具体模块开发（示例）
 ┃ ┣ 📂utils                                    工具目录
 ┃ ┃ ┣ 📜api_limiter.py                         接口限流
 ┃ ┃ ┣ 📜comm_ret.py                            统一 response 封装
 ┃ ┃ ┣ 📜encrypt_data.py                        加密
 ┃ ┃ ┣ 📜handle_regexp.py                       处理正则
 ┃ ┃ ┣ 📜handle_req_param.py                    检查及处理 request 请求参数
 ┃ ┃ ┣ 📜jwt_auth.py                            JWT 编码 及 解码
 ┃ ┃ ┣ 📜operate_elasticsearch.py               操作 elasticsearch 实例
 ┃ ┃ ┣ 📜operate_minio.py                       操作 minio 实例
 ┃ ┃ ┣ 📜operate_mongodb.py                     操作 mongodb 实例
 ┃ ┃ ┣ 📜operate_numeric.py                     操作 numeric 实例
 ┃ ┃ ┣ 📜operate_redis.py                       操作 redis 实例
 ┃ ┃ ┣ 📜opt_redis_sentinel.py                  操作 redis_sentinel 实例
 ┃ ┃ ┣ 📜resp_code.py                           response 状态码（自行扩展）
 ┃ ┃ ┗ 📜sys_access_log.py                      系统日志
 ┃ ┗ 📜app.py                                   项目基本设置
 ┣ 📜.dockerignore                              Docker 构建忽略文件及目录
 ┣ 📜.gitignore                                 git 追踪忽略文件及目录
 ┣ 📜.python-version                            python 版本
 ┣ 📜Dockerfile                                 Docker 构建文件
 ┣ 📜README.md                                  说明
 ┣ 📜docker-compose.yml                         docker-compose 配置文件
 ┣ 📜main.py                                    项目启动文件
 ┣ 📜pyproject.toml                             项目的元数据
 ┗ 📜uv.lock                                    项目依赖项锁定文件
```

### 构建
```bash
docker build -f Dockerfile -t 'fastapi_template_uv:1.0' .
```

### 运行
```bash
docker-compose up -d
```
