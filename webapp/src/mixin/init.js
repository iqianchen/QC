import {dateFormat} from "@/static/js/format.js"

const initMixin = {
  filters: {
    // 日期格式化
    dateFormat(value) {
      if (!value && !isNaN(Date.parse(value))) return ''
      return dateFormat('yyyy-MM-dd hh:mm:ss', new Date(value))
    }
  },
  // 自定义指令
  directives: {
    focus: {
      // 当被绑定的元素插入到DOM中时
      inserted: el => {
        el.focus()
      }
    }
  }
}

export default initMixin