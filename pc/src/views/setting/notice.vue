<template>
  <div id="notice">
    <SimpleTable 
      :option="option" 
      :columns="columns"
      ref="simpleTable"
      @deleteRow="deleteRow"
      @submit="submit"
      @addClick="add_click">

      <div slot="detailPage">
        <!-- 测试 -->
        <div class="row">
          <span class="label">标题</span>
          <Input v-model="data.title" size="small" />
        </div>
        <div class="row">
          <span class="label">日期范围</span>
          <div class="date-group">
            <DatePicker 
              class="date-picker" 
              type="date"
              size="small"
              :value="data.startDate" 
              placeholder="开始日期">
            </DatePicker>
            <span class="line"></span>
            <DatePicker 
              class="date-picker" 
              type="date" 
              size="small"
              :value="data.endDate"
              placeholder="结束日期">
            </DatePicker>
          </div>
        </div>
        <div id="editor"></div>
      </div>
    </SimpleTable>
  </div>
</template>

<script>
import SimpleTable from '#/SimpleTable';
import E from 'wangeditor'

export default {
  name: 'notice',
  components: {
    SimpleTable
  },
  mounted() {
    this._initEditor();
  },
  data() {
    return {
      option: {
        page: 'notice',
        width: 700,
        icon: 'ios-pricetags',
        placeholder: '请输入通知标题',
      },
      columns: [
        {
          key: 'title',
          title: '通知标题'
        }, {
          key: 'startDate',
          title: '通知开始日期'
        }, {
          key: 'endDate',
          title: '通知结束日期'
        }
      ],
      data: {
        title: '',
        startDate: '',
        endDate: '',
        content: ''
      },
      editor: ''
    }
  },
  methods: {
    _initEditor() {
      let editor = new E('#editor');
      // 自定义菜单
      editor.customConfig.menus = [
        'head',  // 标题
        'bold',  // 粗体
        'fontSize',  // 字号
        'fontName',  // 字体
        'italic',  // 斜体
        'underline',  // 下划线
        'strikeThrough',  // 删除线
        'foreColor',  // 文字颜色
        'backColor',  // 背景颜色
        'link',  // 插入链接
        'list',  // 列表
        'justify',  // 对齐方式
        'quote',  // 引用
        'image',  // 插入图片
        'code',  // 插入代码
        'undo',  // 撤销
        'redo'  // 重复
      ]  
      // editor.customConfig.onchange = function(){
      // }
      // editor.customConfig.uploadImgShowBase64 = true
      editor.customConfig.uploadImgServer = '/upload';
      editor.create();
      this.editor = editor;
      // editor.txt.html()   // 设置编辑器内容
      // editor.txt.append() // 继续追加内容
      // editor.txt.clear()  // 清空内容
    },
    // 删除行
    deleteRow(row) {
      console.log('row', row)
      this.$refs.simpleTable.refresh()
    },
    add_click() {
      this.data = {
        userName: ''
      }
      this.editor.txt.clear()
    },
    submit() {
      let editorHtml = this.editor.txt.html()
      let escapeHtml = escape(editorHtml)   // 对富文本内容进行转码转码
      this.data.content = escapeHtml
    }
  }
}
</script>


<style lang="less">
.ivu-date-picker  .ivu-select-dropdown {
  z-index: 100000;
}
.date-picker {
  width: 130px;
}
#editor {
  margin: 15px 0 0;
  height: 350px;
}
</style>


