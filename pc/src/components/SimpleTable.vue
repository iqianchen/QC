<template>
  <div id="simpleTable">
    <div class="simple-filter">
      <Select
        class="filter-search"
        remote
        filterable
        v-model="keyword"
        :prefix="option.icon"
        :remote-method="getDataList"
        :loading="searchLoading"
        :placeholder="option.placeholder">
        <Option v-for="item in dataList" :key="item.id" :value="item.id"> {{item.value}}</Option>
      </Select>
      <div>
        <ButtonGroup>
          <Button icon="md-add" @click="add_click">新增</Button>
          <Button icon="md-refresh" @click="getData">刷新</Button>
        </ButtonGroup>
      </div>
    </div>
    <div class="simple-content">
      <Table 
        v-if="tableHeight > 0" 
        :columns="TColumns" 
        :data="TData" 
        :height="tableHeight"
        :loading="loading"
        highlight-row>
      </Table>
    </div>
    <div class="simple-footer">
      <Page 
        :current="attr.pageIndex"
        :total="attr.total"
        :page-size="attr.pageSize"
        size="small"
        show-total
        show-elevator 
        show-sizer
        @on-change="changePage"
        @on-page-size-change="changePageSize">
      </Page>
    </div>

    <Modal
      v-model="showModal"
      :width="option.width || 520"
      :mask-closable="false"
      :title="detailTitle"
      @on-ok="submit"
      @on-cancel="showModal = false">
      <slot name="detailPage"></slot>
    </Modal>
  </div>
</template>

<script>
export default {
  props: {
    option: {
      type: Object,
      default() {
        return {}
      }
    },
    columns: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {
      TColumns: [],
      TData: [],
      attr: {
        pageIndex: 1,
        pageSize: 20,
        total: 0
      },
      tableHeight: 0,
      keyword: '',
      dataList: [],
      type: 'add',
      loading: false,       // 表格数据加载时显示
      searchLoading: false, // 搜索数据加载时显示
      showModal: false      // 显示详情界面
    }
  },
  created() {
    this._initTableHeight();
    this._initColumns()
    this.getData()
  },
  // mounted() {
  //   this._initTableHeight()
  // },
  methods: {
    // 初始化表格高度
    _initTableHeight() {
      let bodyHeight = document.body.clientHeight;    // body的高度
      let pageHeight = bodyHeight - (32 + 16);        // 减去标签页的高度
      let tableHeight = pageHeight - (70 + 60);       // 减去搜索区域和分页区域的高度
      this.tableHeight = tableHeight
    },
    // 初始化表格列
    _initColumns() {
      let tmpColumns = this.columns;
      if (tmpColumns[0].type !== 'index') {
        tmpColumns.unshift({    // 添加序号列
          type: 'index',
          width: 70,
          title: '序号',
          align: 'center'
        })
        tmpColumns.push({     // 添加编辑和删除功能
          key: 'action',
          title: '操作',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {    // 属性
                  type: 'primary',
                  size: 'small',
                  icon: 'md-open'
                },
                style: {    // 样式
                  marginRight: '8px'
                },
                on: {     // 事件
                  click: () => {
                    console.log('1111')
                    this.type = 'update';
                    this.showModal = true;
                    this.$emit('getDetail', params)
                  }
                }
              }, '编辑'),
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small',
                  icon: 'md-trash'
                },
                on: {
                  click: () => {
                    this.deleteRow(params.row)
                  }
                }
              }, '删除')
            ])
          }
        })
      }
      this.TColumns = tmpColumns;
    },
    // 刷新表格数据
    refresh() {
      this.getData();
    },
    // 获取表格数据
    async getData() {
      this.loading = true;

      let data = [];
      console.log('this.option.page', this.option.page)
      switch (this.option.page) {
        case 'notice':
          data = [{
            title: '测试标题',
            content: '测试内容',
            startDate: '2019-10-10',
            endDate: '2019-10-25'
          }]
          break;
        case 'user':
          data = [{
            name: '测试',
            number: '001',
            post: 1
          }]
          break;
        case 'deparment':
          data = [{
            supplier: '测试供应商1,测试供应商2,测试供应商3,测试供应商4,测试供应商5',
            testType: 1,
            rate: 20,
            enable: true,
            isResult: false
          }]
          break;
      }
      setTimeout(() => {
        this.TData = data
        this.attr.total = 1;
        this.loading = false;
      }, 800)
      // if (this.loading) return;
      // this.loading = true;
      // try {
      //   let result = await this.http.post('/', params);
      //   this.loading = false;
      //   this.TData = result.data;
      //   this.attr.total = result.total;
      // } catch(e) {
      //   this.loading = false;
      //   console.log('e', e)
      // }
    },
    // 删除行
    deleteRow(params) {
      this.$Modal.confirm({
        title: '提示',
        content: '您确定要删除？',
        onOk: () => {
          this.$emit('deleteRow', params)
        }
      })
    },
    // 点击新增
    add_click() {
      this.type = 'add';
      this.showModal = true;
      this.$emit('addClick');
    },
    getDataList() {
      this.searchLoading = true;
      setTimeout(() => {
        this.dataList = [
          {
            id: 1,
            value: '测试数据'
          }, {
            id: 2,
            value: '测试供应商'
          }
        ]
        this.searchLoading = false;
      }, 1200)
    },
    submit() {
      this.$emit('submit');
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
    }
  },
  computed: {
    detailTitle() {
      let value = '';
      switch (this.type) {
        case 'add':
          value = '新增';
          break;
        case 'update':
          value = '修改';
          break;
      }
      return value;
    }
  }
}
</script>

<style lang="less">
#simpleTable {
  .simple-filter {
    height: 60px;
    padding: 8px 10px 20px;
    box-sizing: border-box;
    display: flex;
    justify-content: space-between;
    .filter-search {
      width: 200px;
    }
  }
  .simple-footer {
    height: 60px;
    padding: 10px 0;
    box-sizing: border-box;
    text-align: center;
  }
}
</style>
