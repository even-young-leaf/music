# 音乐网站 Vue 前端

这是音乐网站的 Vue 前端部分，与 Django 后端集成。

## 项目结构

```
frontend/
  ├── src/                # 源代码目录
  │   ├── App.vue        # 根组件
  │   ├── main.js        # 入口文件
  │   ├── router/        # 路由配置
  │   ├── store/         # Vuex 状态管理
  │   └── views/         # 页面组件
  ├── public/            # 静态资源
  ├── package.json       # 项目依赖
  └── vue.config.js      # Vue 配置
```

## 安装依赖

```bash
cd frontend
npm install
```

## 开发模式

```bash
npm run serve
```

开发服务器将在 http://localhost:8080 启动，并自动代理 API 请求到 Django 后端。

## 构建生产版本

```bash
npm run build
```

构建后的文件将输出到 Django 项目的静态文件目录中。

## 访问 Vue 版本

在 Django 项目中，可以通过以下 URL 访问 Vue 版本的应用：

```
http://localhost:8000/?vue=1
```

## 与 Django 集成

- Vue 应用通过 API 与 Django 后端通信
- API 端点定义在 `index/api_views.py` 中
- Vue 路由与 Django URL 保持一致，以便平滑过渡

## 逐步迁移策略

1. 从简单页面开始迁移到 Vue
2. 保留现有 Django 模板，同时提供 Vue 版本
3. 组件化开发，逐步替换 Django 模板
4. API 化数据获取，减少对 Django 模板渲染的依赖