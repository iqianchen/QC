import qs from 'qs'
import axios from 'axios'
import Setting from '@/config/Setting.js'

const myAxios = axios.create({
  baseURL: Setting.baseURL,
  timeout: 5000,
  headers: { 'content-type': 'application/x-www-form-urlencoded' }
})

class Http {
  constructor() {}
  // GET请求
  get(url, data = {}, loading = false) {
    return this.requestAll(url, data, 'GET', loading)
  }
  // POST请求
  post(url, data, loading = false) {
    let jsonData = qs.stringify(data)
    return this.requestAll(url, jsonData, 'POST', loading)
  }
  // PUT请求
  put(url, data, loading = false) {
    let jsonData = qs.stringify(data)
    return this.requestAll(url, jsonData, 'PUT', loading)
  }
  // DELETE请求
  delete(url, data = {}, loading = false) {
    return this.requestAll(url, data, 'DELETE', loading)
  }

  requestAll(url, data, method, loading) {
    if (loading) {
      // 自定义开启loading时需要执行的代码
    }
    return new Promise((resolve, reject) => {
      myAxios({
        url,
        data,
        method
      }).then( res => {
        if (loading) {
          // 如果开启了loading需要结束loading
        }
        if (res.data.code === 0) {
          resolve(res.data.data)
        } else if (res.data.code === 1) {
          let errorMsg = '未知错误'
          if (res.data.message) {
            switch (typeof (res.data.message)) {
              case 'string':
                errorMsg = res.data.message;
                break;
              case 'object':
                errorMsg = JSON.stringify(res.data.message)
                break;
              default:
                break;
            }
          }

          if (dd) {
            dd.device.notification.alert({
              message: errorMsg,
              title: '错误提示',
              buttonName: '确定'
            })
          }
          reject(errorMsg)
        }
      }).catch(err => {
        let errMsg = '发送请求的时候遇到一个错误，错误详情为：' + err
        new Error(errMsg)
        if (loading) {
          // 如果开启了loading需要结束loading
        }
      })
    })
  }
}

export default new Http()