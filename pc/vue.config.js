const path = require('path')
function resolve(dir) {
  return path.join(__dirname, dir)
}

module.exports = {
  publicPath: '/',  // 项目路径
  outputDir: 'dist',  //  构建输出目录
  assetsDir: './static',  // 静态资源目录
  lintOnSave: true,   // 是否开启eslint保存检测, 有效值：ture | false | 'error'
  runtimeCompiler: true, // 运行时版本是否需要编译
  transpileDependencies: [], // 默认babel-loader忽略mode_modules，这里可增加例外的依赖包名
  productionSourceMap: false, // 是否在构建生产包时生成 sourceMap 文件，false将提高构建速度
  chainWebpack: (config) => {
    config.resolve.alias  // 修改文件引入自定义路径
      .set('@', resolve('src'))
      .set('#', resolve('src/components'))
      .set('v', resolve('src/views'))
      .set('js', resolve('src/assets/js'))
      .set('less', resolve('src/assets/less'))
  }
}