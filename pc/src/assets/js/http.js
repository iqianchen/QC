import axios from 'axios'
import qs from 'qs'       // 序列化请求数据, 视服务端的要求需不需要
import Setting from '@/config/setting.js'

// 创建axios实例 axiso的一些基础参数配置
const service = axios.create({
  baseURL: Setting.baseUrl,
  timeout: 5000    // 超时时间
})

// 传参拦截器
service.interceptors.request.use(
  config => {
    // 判断为post请求，序列化传来的参数
    if (config.method === 'post' || config.method === 'put' || config.method === 'delete') {
      config.data = qs.stringify(config.data)
    }
    return config
  }, error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
// service.interceptors.response.use(
//   res => {
//     return res
//   }, error => {
//     // 请求错误
//     console.log(error)
//     return error
//     // 1.判断请求超时
//     if (error.code === 'ECONNABORTED' && error.message.indexOf('timeout') !== -1) {
//       console.log('请求超时！！！')
//       // 设置请求超时的处理方案
//     }
//     // 2.需要重定向到错误页面
//     const errorInfo = error.response
//     console.log(errorInfo)
//     if (errorInfo) {
//       // 根据错误状态码跳转到相应的页面
//       switch (errorInfo.status) {
//         case 403:
//           break;
//         case 404:
//           break;
//         case 500:
//           break;
//       }
//     }
//     // return Promise.reject(error)
//     return error
//   }
// )

class http {
  constructor() {
    this.loadingDelay = 300,    // 设置请求时间超出多少才显示loading
    this.delayTimeoutId = 0
  }

  // GET请求
  get(url, data = {}, loading = false) {
    return this.requestAll(url, data, 'GET', loading)
  }
  // POST请求
  post(url, data, loading = false) {
    return this.requestAll(url, data, 'POST', loading)
  }
  // PUT请求
  put(url, data, loading = false) {
    return this.requestAll(url, data, 'PUT', loading)
  }
  // DELETE请求
  delete(url, data = {}, loading = false) {
    return this.requestAll(url, data, 'DELETE', loading)
  }

  requestAll(url, data, method, loading) {
    if (loading) {
      this.delayTimeoutId = setTimeout(() => {
        // 这里添加loading状态

      }, this.loadingDelay)
    }
    return new Promise((resolve, reject) => {
      service({
        url,
        data,
        method
      }).then( res => {
        if (loading) {
          clearTimeout(this.delayTimeoutId)
          // 这里结束loading状态
        }
        // 与后台商定好返回成功和返回失败的字段
        if (res.data && res.data.data) {
          // 成功返回数据
          resolve(res.data.data)
        } else {
          // 服务器返回错误信息
          reject(res.data.message || '遇到一个未知的错误')
        }
      }).catch( err => {
        console.log('err', err)
        if (loading) {
          clearTimeout(this.delayTimeoutId)
          // 这里结束loading状态
        }
        // 提示错误信息
        let errMsg = '发送请求的时候遇到一个错误，错误详情为：' + err
        reject(errMsg)
        new Error(errMsg)
      })
    })
  }
}

// 导出
export default new http()