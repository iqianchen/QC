<template>
  <!-- 表格模型 -->
  <div id="tableModel">
      <!-- <Card> -->
        <!-- 表格头部 -->
        <div v-if="!hideHeader" slot="title" class="table-header">
          <div class="table-title">
            <Icon type="ios-stats" />
            <span v-text="attr.title"></span>
            <slot name="message"></slot>
          </div>
          <div class="table-action">
            <ButtonGroup>
              <Button 
                v-for="item in buttonData" 
                :key="item.text" 
                :icon="item.icon" 
                @click="buttonMethods(item.methods)">
                {{item.text}}
              </Button>
              <slot name="custom-button"></slot>
            </ButtonGroup>
          </div>
        </div>
        <!-- 标签页(多选时启用) -->
        <!-- <div class="tag-box" v-if="selectionChange">
          <span class="tips" v-if="activeRows.length === 0">暂无选中的数据...</span>
          <Tag 
          v-for="item in activeRows" 
          :key="item.id" 
          :name="item.id" 
          closable
          @on-close="handleClose">{{item.resellerName}}</Tag>
        </div> -->
        <!-- 表格 -->
        <div class="table-content">
          <Table 
            :columns="TColumns" 
            :data="TData" 
            :height="attr.height || this.tableHeight"
            :loading="loading"
            :stripe="true"
            :border="true"
            
            size="small"
            ref="selection"
            
            @on-row-click="clickRow"
            >
          </Table>

          <!-- :highlight-row="!selectionChange"
          :row-class-name="rowClassName"
          @on-select="onSelect"
          @on-select-cancel="onSelectCancel"
          @on-select-all="onSelectAll"
          @on-select-all-cancel="onSelectAllCancel" -->
        </div>
        <!-- 底部分页区域 -->
        <div class="table-footer">
          <Page 
            :current="attr.pageIndex"
            :total="attr.total"
            :page-size="attr.pageSize"
            size="small"
            show-total
            show-elevator 
            @on-change="changePage"
            @on-page-size-change="changePageSize">
          </Page>
        </div>
      <!-- </Card> -->
  </div>
</template>

<script>
import ExportExcel from 'js/exportExcel.js';
import http from 'js/http.js';
export default {
  name: 'tableModel',
  data() {
    return {
      buttonData: [],   // 功能按钮数据
      loading: false,   // 加载状态
      tableHeight: 0,   // 表格高度
      TColumns: [],     // 表格列
      TData: [],        // 表格数据
      attr: {},         // 表格属性
      activeRows: []    // 选中行数据
    }
  },
  props: {
    hideHeader: {   // 是否隐藏表格头部  默认显示
      type: Boolean,
      default: false
    },
    action: {   // 表格的功能按钮  默认只有刷新
      type: Array,
      default() {
        return []
      }
    },
    columns: {  // 表格列
      type: Array,
      default() {
        return []
      }
    },
    options: {  // 设置
      type: Object,
      default() {
        return {}
      }
    }
  },
  created() {
    this._initTableHeight()
  },
  mounted() {
    this._initOptions()
    this._initButton()
    this.getData()
  },
  methods: {
    // 初始化表格高度
    _initTableHeight() {
      let bodyHeight = document.body.clientHeight;    // body的高度
      let pageHeight = bodyHeight - (32 + 16);        // 减去标签页的高度
      let tableHeight = pageHeight - (10 + 40 + 25 + 10)
      // console.log('pageHeight', pageHeight)
      this.tableHeight = tableHeight;
    },
    // 初始化表格选项
    _initOptions() {
      let defaultOptions = {    // 默认值
        type: 'post',
        title: '',          // 表格标题
        index: true,        // 是否启用索引
        selection: false,   // 是否启用多选
        params: {},         // 固定参数
        pageIndex: 1,
        pageSize: 20,
        total: 0
      }
      this.attr = Object.assign({}, defaultOptions, this.options)

      this._initColumn()
    },
    // 初始化表格列
    _initColumn() {
      let tmpColumns = this.columns;
      tmpColumns.forEach(item => {
        item.tooltip = true;    // 文本将不换行，超出部分显示为省略号，并用 Tooltip 组件显示完整内容
      })
      if (this.attr.index && (tmpColumns[0].type !== 'index' || tmpColumns[1].type !== 'index')) {  // 显示序号
        tmpColumns.unshift({
          type: 'index',
          width: 70,
          title: '序号',
          align: 'center'
        })
      }
      if (this.attr.selection && tmpColumns[0].type !== 'selection') {  // 启用多选
        tmpColumns.unshift({
          type: 'selection',
          width: 50,
          align: 'center'
        })
      }

      this.TColumns = tmpColumns;
    },
    // 初始化表格功能按钮
    _initButton() {
      if (this.hideHeader) return;
      let tmpAction = this.action;
      if (tmpAction.indexOf('refresh') === -1) tmpAction.push('refresh');   // 默认启用刷新按钮
      let tmpButton = [];
      tmpAction.forEach(item => {
        switch (item) {
          case 'refresh': // 刷新
            tmpButton.push({
              sort: 1,
              icon: 'md-refresh',
              text: '刷新',
              methods: 'refresh'
            })
            break;
          case 'upload':  // 导入
            tmpButton.push({
              sort: 2,
              icon: 'ios-cloud-upload-outline',
              text: '导入',
              methods: 'uploadFile'
            })
            break;
          case 'downLoad':  // 导出
            tmpButton.push({
              sort: 3,
              icon: 'ios-cloud-download-outline',
              text: '导出',
              methods: 'downloadExl'
            })
            break;
          case 'filter':    // 过滤
            tmpButton.push({
              sort: 4,
              icon: 'ios-funnel',
              text: '筛选',
              methods: 'filter_click'
            })
        }
      })
      this.buttonData = tmpButton;
    },
    // 传递按钮事件
    buttonMethods(value) {
      switch(value) {
        case 'downloadExl':
          ExportExcel.export({
            headers: this.columns,
            data: this.TData
          }, this.attr.title || '未命名')
          break;
        case 'refresh':
          this.getData();
          break;
        default:
          this.$emit(value)
      }
    },
    // 获取表格数据
    async getData(params2 = {}) {
      if (this.loading) return;
      if (this.attr.url) {
        this.loading = true;
        let params = Object.assign({}, this.attr.params, params2, {
          pageIndex: this.attr.pageIndex,
          pageSize: this.attr.pageSize
        })
        try {
          let result = await http.post(this.attr.url, params);
          this.loading = false;
          let tmpData = this._handleData(result.data);
          this.TData = tmpData;
          this.attr.total = result.total;
        } catch (e) {
          this.loading = false;
        }
      }
    },
    // 处理返回数据
    _handleData(data) {
      if (!data) return [];
      if (this.options.selection === true) {
        // 开启多选后， 对已选数据添加选中状态
        data.forEach(item => {
          this.activeRows.map(value => {
            if (item.id === value.id) {
              item._checked = true
            }
          })
        })
      }
      return data;
    },
    // 改变页码
    changePage(current) {
      this.attr.pageIndex = current;
      this.getData()
    },
    // 切换每页条数时的回调
    changePageSize(pageSize) {
      this.attr.pageIndex = 1;
      this.attr.pageSize = pageSize;
      this.getData();
    },
    // 在多选模式下有效，选中某一项时触发
    onSelect(selection, row) {
      this.activeRows.push(row);
    },
    // 在多选模式下有效，取消选中某一项时触发
    onSelectCancel(selection, row) {
      let currentIndex = this.activeRows.findIndex(item => item.id === row.id);
      if (currentIndex !== -1) this.activeRows.splice(currentIndex, 1);
    },
    // 在多选模式下有效，点击全选时触发
    onSelectAll(selection) {
      selection.map(item => {
        let result = this.activeRows.filter(value => item.id === value.id)
        if (result.length === 0) this.activeRows.push(item)
      })
    },
    // 在多选模式下有效，点击取消全选时触发
    onSelectAllCancel() {
      let tmpIndex = 0;
      let tmpRows = this.activeRows.slice();    // 新建一个副本
      this.activeRows.map((item, index) => {
        let eq = this.TData.findIndex(value => item.id === value.id);
        if (eq !== -1) {
          tmpRows.splice(index-tmpIndex, 1)
          tmpIndex++
        }
      })
      this.activeRows = tmpRows;
    },
    // 定义行样式
    rowClassName(rowData) {
      for(let i = 0; i < this.activeRows.length; i++) {
        if (rowData.projectid && this.activeRows[i].projectid === rowData.projectid) return 'selected-row';
      }
    },
    // 点击表格行触发的事件
    clickRow(rowData, index) {
      if (this.TColumns[0].type === 'selection') {
        this.$refs.selection.toggleSelect(index);
      } else {
        this.activeRows = [rowData]
      }
    },
    // 关闭标签页
    handleClose($event, name) {
      let index = this.TData.findIndex(item => item.id === name)
      if (index !== -1) this.$refs.selection.toggleSelect(index);

      let index2 = this.activeRows.findIndex(item => item.id === name)
      if (index2 !== -1) this.activeRows.splice(index2, 1)
    },
    // 获取当前选中行
    getActiveRows() {

    }
  },
  // computed: {
  //   selectionChange() {   // 监听是否启用多选
  //     return this.options.selection;
  //   }
  // },
  // watch: {
  //   selectionChange(value) {   // 开启或关闭多选
  //     // 清空所有已选值
  //     this.activeRows = [];
  //     this.$refs.selection.selectAll(false);

  //     if (value === true) {   // 启用多选时新增复选框列
  //       if (this.TColumns[0] && this.TColumns[0].type === 'selection') return;
  //       this.TColumns.unshift({
  //         type: 'selection',
  //         width: 50,
  //         align: 'center'
  //       })
  //     } else {    // 停用多选时删除复选框列
  //       if (this.TColumns[0] && this.TColumns[0].type === 'selection') {
  //         this.TColumns.shift()
  //       }
  //     }
  //   }
  // }
}
</script>

<style lang="less">
@import '~less/color.less';
#tableModel {
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: @blueLight;
    height: 40px;
    padding: 2px 6px 0;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    .table-title {
      font-size: 18px;
      >span {
        margin-left: 8px;
      }
    }
  }

  .tag-box {
    height: 58px;
    border: 1px solid @ghostWhite;
    padding: 3px 5px;
    overflow-y: auto;
    margin-bottom: 8px;
  }

  .table-footer {
    margin: 10px 0;
    .ivu-page {
      text-align: center;
    }
  }

  .ivu-table .selected-row {
    background: @olive;
    color: #fff;
  }
  .ivu-table .selected-row td {
    background-color: transparent;
    color: inherit;
  }
  .ivu-table-small td {
    height: 35px;
  }
}
</style>

