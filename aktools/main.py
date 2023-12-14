# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/28 15:05
Desc: 主程序入口文件
"""
from aktools.utils import get_latest_version
from aktools.datasets import get_favicon_path, get_homepage_html
from aktools.core.api import app_core, templates
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import uvicorn
import aktools
import akshare
import os
import sys

# 添加 package 查找路径，该行必须在前面，否则不能导入相关的模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# from login import app_user_login

favicon_path = get_favicon_path(file="favicon.ico")
html_path = get_homepage_html(file="homepage.html")


app = FastAPI(
    title="欢迎访问 AKTools 为 AKShare 打造的 HTTP API 在线文档",
    description="AKTools 是 AKShare 的 HTTP API 工具, 主要目的是使 AKShare 的数据接口部署到服务器，从而让用户通过 HTTP 访问相关接口来获取所需要的数据",
    version=akshare.__version__,
    redoc_url=None,
)


@app.get("/", tags=["主页"], description="主要展示网站首页", summary="网站首页")
async def get_homepage(request: Request):
    return templates.TemplateResponse(
        "homepage.html",  # 此处的 homepage.html 可以自定义，主要采用 jinja2 模版
        context={
            "request": request,
            "ip_address": request.headers["host"],
            "ak_current_version": akshare.__version__,
            "at_current_version": aktools.__version__,
            "ak_latest_version": get_latest_version("akshare"),
            "at_latest_version": get_latest_version("aktools"),
        },
    )


origins = ["*"]  # 此处设置可以访问的协议，IP和端口信息

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_core, prefix="/api", tags=["数据接口"])
# app.include_router(app_user_login, prefix="/auth", tags=["登录接口"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, debug=True)
