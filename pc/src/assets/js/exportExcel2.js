import XLSX from 'xlsx';
class ExportExcel {
  constructor() {

  }

  creatRef(header, data) {
    const _header = header.map((item, i) => {
      return Object.assign({}, {
        key: item.key,
        title: item.title,
        position: String.fromCharCode(65 + i) + 1
      })
    }).reduce((prev, next) => {
      return Object.assign({}, prev, {
        [next.position]: { 
          key: next.key, 
          v: next.title
        }
      })
    })

    const _data = data.map((item, i) => {
      return header.map((key, j) => {
        let defaultValue = '', type = 's';    // 给每个单元格设置默认值
        switch(key.type) {                // 判断当前单元格的类型
          case 'number':
            type = 'n';
            defaultValue = 0;
            break;
          case 'date':
            type = 'd';
            break;
          case 'boolean':
            type = 'b';
            break;
          default:
            type = 's'
        }
        return Object.assign({}, {
          content: item[key.key] || defaultValue,
          type: type,
          position: String.fromCharCode(65 + j) + (i + 2)
        })
      })
    }).reduce((prev, next) => {
      return prev.concat(next)
    }).reduce((prev, next) => {
      return Object.assign({}, prev, {
        [next.position]: { 
          v: next.content,
          t: next.type
        }
      })
    }, {})

    // 合并 headers 和 data
    var output = Object.assign({}, _headers, _data);
    // 获取所有单元格的位置
    var outputPos = Object.keys(output);
    // 计算出范围 ,["A1",..., "H2"]
    var ref = `${outputPos[0]}:${outputPos[outputPos.length - 1]}`;
  }
}