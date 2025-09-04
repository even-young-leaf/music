module.exports = {
  // 输出到Django的静态文件目录
  outputDir: '../static/vue',
  
  // 设置publicPath，确保Django能找到静态资源
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/vue/'
    : '/',
    
  // 关闭eslint检查
  lintOnSave: false,
  
  // 配置开发服务器代理，用于开发时访问Django API
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
};