#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@File :  api_json.py  
@Desc :  接口文档: 来源于 openapi.json
'''


API_JSON = {
    "openapi": "3.0.2",
    "info": {
        "title": "xxx",
        "description": "xxx",
        "version": "v1.0"
    },
    "paths": {
        "/api/v1.0/user_auth/login": {
            "post": {
                "tags": [
                    "认证"
                ],
                "summary": "登录",
                "description": "用户登录  \ncode 返回 1200 重新登录;  \ncode 返回 200 时, resp 中返回 jwt 及 refresh_jwt 信息;  \njwt 用于验证用户登录;  \n当 访问系统所有需要认证的接口并返回 1102 时, 使用 refresh_jwt 刷新 jwt 及 refresh_jwt 信息;\n当返回 1101 时, jwt 生成异常, 再次发起请求 (基本不需要)\n\n即 code == 1102 , 需刷新 jwt;  \ncode == 1200 , 需重新登录后跳转;  \ncode == 1101 , 再次请求; (基本不需要)  ",
                "operationId": "___api_v1_0_user_auth_login_post",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/Body____api_v1_0_user_auth_login_post"
                            }
                        }
                    },
                    "required": True
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/v1.0/user_auth/refresh_token": {
            "get": {
                "tags": [
                    "认证"
                ],
                "summary": "刷新 Token 信息",
                "operationId": "___Token____api_v1_0_user_auth_refresh_token_get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "refresh_jwt",
                            "minLength": 1,
                            "type": "string"
                        },
                        "name": "refresh_jwt",
                        "in": "query"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [
                    {
                        "OAuth2PasswordBearer": []
                    }
                ]
            }
        },
        "/api/v1.0/user/": {
            "get": {
                "tags": [
                    "示例接口"
                ],
                "summary": "Get User Info",
                "operationId": "get_user_info_api_v1_0_user__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "security": [
                    {
                        "OAuth2PasswordBearer": []
                    }
                ]
            }
        },
        "/api/v1.0/info/dep_security_1": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Dep Security 1",
                "operationId": "dep_security_1_api_v1_0_info_dep_security_1_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "security": [
                    {
                        "OAuth2PasswordBearer": [
                            "info1"
                        ]
                    }
                ]
            }
        },
        "/api/v1.0/info/dep_security_2": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Dep Security 2",
                "operationId": "dep_security_2_api_v1_0_info_dep_security_2_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                },
                "security": [
                    {
                        "OAuth2PasswordBearer": [
                            "info2"
                        ]
                    }
                ]
            }
        },
        "/api/v1.0/info/download_csv_use_IO": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Download Csv Use Io",
                "operationId": "download_csv_use_IO_api_v1_0_info_download_csv_use_IO_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/api/v1.0/info/download_csv_use_generator": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Download Csv Use Generator",
                "operationId": "download_csv_use_generator_api_v1_0_info_download_csv_use_generator_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/api/v1.0/info/download_excel_use_IO": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Download Excel Use Io",
                "operationId": "download_excel_use_IO_api_v1_0_info_download_excel_use_IO_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/api/v1.0/info/opt_redis_sentinel": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Opt Redis Sentinel",
                "operationId": "opt_redis_sentinel_api_v1_0_info_opt_redis_sentinel_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        },
        "/api/v1.0/info/opt_redis": {
            "get": {
                "tags": [
                    "示例接口Security/scopes"
                ],
                "summary": "Opt Redis",
                "operationId": "opt_redis_api_v1_0_info_opt_redis_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {}
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Body____api_v1_0_user_auth_login_post": {
                "title": "Body____api_v1_0_user_auth_login_post",
                "required": [
                    "username",
                    "password"
                ],
                "type": "object",
                "properties": {
                    "grant_type": {
                        "title": "Grant Type",
                        "pattern": "password",
                        "type": "string"
                    },
                    "username": {
                        "title": "Username",
                        "type": "string"
                    },
                    "password": {
                        "title": "Password",
                        "type": "string"
                    },
                    "scope": {
                        "title": "Scope",
                        "type": "string",
                        "default": ""
                    },
                    "client_id": {
                        "title": "Client Id",
                        "type": "string"
                    },
                    "client_secret": {
                        "title": "Client Secret",
                        "type": "string"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            }
        },
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "scopes": {
                            "emp": "emp",
                            "cus": "cus"
                        },
                        "tokenUrl": "/api/v1.0/user_auth/login"
                    }
                }
            }
        }
    }
}
