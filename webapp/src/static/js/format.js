// 日期格式化
function dateFormat(fmt,date) {
  var o = {   
    "M+" : date.getMonth()+1,                 //月份   
    "d+" : date.getDate(),                    //日   
    "h+" : date.getHours(),                   //小时   
    "m+" : date.getMinutes(),                 //分   
    "s+" : date.getSeconds(),                 //秒   
    "q+" : Math.floor((date.getMonth()+3)/3), //季度   
    "S"  : date.getMilliseconds()             //毫秒   
  }
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length))
  for(var k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length))) 
  return fmt
}

// 数字格式化
function numberFormat(num, length) {
  if (isNaN(num)) return
  var num = (num || 0).toString(), result = '';
  var integer = '', decimal = ''
  // 判断是否有小数
  if (num.indexOf('.') !== -1) {
    integer = num.split('.')[0]
    decimal = num.split('.')[1]
    var newdecimal = '';
    if (decimal.length < length) {    // 小数位不够则补0
      for (let i = 0; i < length-decimal.length; i++) {
        newdecimal += '0' 
      }
    }else if(decimal.length > length) {   // 小数位超出则截取
      decimal = decimal.slice(0,length)
    }
    decimal = decimal+newdecimal
  }else {
    integer = num
    for (let i = 0; i < length; i++) {
      decimal += '0' 
    }
  }

  while (integer.length > 3) {    // 整数部分每隔3位做一次分隔
    result = ',' + integer.slice(-3) + result;
    integer = integer.slice(0, integer.length - 3);
  }
  if (integer.length == 1 && isNaN(integer) && result) {
    result = result.substr(1);
  }
  num = integer + result + '.' + decimal
  return num;
}


export {dateFormat, numberFormat}