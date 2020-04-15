<template>
  <div class="layout">
    <div class="layout-left">
      <div class="list-search">
        <Select
          class="filter-search"
          remote
          filterable
          v-model="keyword"
          :prefix="option.icon"
          :remote-method="getsearchList"
          :loading="searchLoading"
          :placeholder="option.placeholder">
          <Option v-for="item in searchList" :key="item.id" :value="item.id"> {{item.value}}</Option>
        </Select>
      </div>
      <ul class="list-content">
        <li 
          v-for="(item, index) in listData" 
          :key="item.id" 
          @click="selectedItem(item)"
          :class="activeItem == item.id ? 'list-acitve' : ''">
          <span class="list-index" v-text="index + 1"></span>
          <span v-text="item.value"></span>
        </li>
      </ul>
      <div class="list-page"></div>
    </div>
    <div class="layout-right">
      <div class="layout-action">
        <ButtonGroup v-if="!isEdit">
          <Button icon="md-add" @click="add_click">新增</Button>
          <Button icon="md-open" @click="update_click">编辑</Button>
          <Button icon="md-trash" @click="delete_click" v-if="activeItem !== -1">删除</Button>
        </ButtonGroup>
        <ButtonGroup v-if="isEdit">
          <Button @click="cancel_click" icon="ios-arrow-back">取消</Button>
          <Button @click="save_click" icon="md-checkbox-outline">保存</Button>
        </ButtonGroup>
      </div>

      <div class="layout-content">
        <div class="row">
          <span class="label">选择类别</span>
          <Select class="row-select" v-model="data.typeId">
            <Option v-for="item in typeList" :key="item.id" :value="item.id">{{ item.name }}</Option>
          </Select>
        </div>
        <div class="row">
          <span class="label">检验项目</span>
          <div class="full">
            <Input v-model="tmpText" @on-enter="add_detail"/>
            <Button @click="add_detail" class="add-item" icon="md-add">添加</Button>
          </div>
        </div>
        <div class="project-table" v-if="tableHeight !== 0">
          <Table :columns="TColumns" :data="TData" :height="tableHeight"></Table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      listData: [
        {
          id: 1,
          value: '沙发类'
        }, {
          id: 2,
          value: '软床类'
        }, {
          id: 3,
          value: '床头柜'
        }
      ],
      option: {
        icon: '',
        placeholder: '搜索名称'
      },
      data: {
        typeId: 1
      },
      keyword: '',
      activeItem: -1,
      searchLoading: false,
      isEdit: false,    // 是否进入新增或编辑状态
      searchList: [],
      tmpText: '',
      typeList: [{
        id: 1,
        name: '沙发类'
      }],
      tableHeight: 0,
      TColumns: [
        {
          type: 'index',
          width: 70,
          title: '序号',
          align: 'center'
        },{
          key: 'name',
          align: 'center',
          title: '检验项目'
        }, {
          key: 'action',
          title: '操作',
          width: 70,
          align: 'center',
          render: (h, params) => {
            return h('Icon',{
              props: {
                type: 'ios-trash',
                color: '#ed4014',
                size: 24
              },
              style: {
                cursor: 'pointer'
              },
              on: {
                click: () => {
                  console.log('params', params)
                  this.delete_detail(params.row)
                }
              }
            })
          }
        }
      ], // 表格列
      TData: [{
        name: '测试检验项目'
      }],  // 表格数据
    }
  },
  created() {
    this._initTableHeight();
  },
  methods: {
    // 初始化表格高度
    _initTableHeight() {
      let bodyHeight = document.body.clientHeight;    // body的高度
      let pageHeight = bodyHeight - (32 + 16);        // 减去标签页的高度
      let otherHeight = 160;          // 其他区域的高度
      let tableHeight = pageHeight - otherHeight;
      this.tableHeight = tableHeight
      console.log(bodyHeight, pageHeight, )
    },
    // 获取搜索数据列表
    getsearchList() {
      this.searchLoading = true;
      setTimeout(() => {
        this.searchLoading = false;
        this.searchList = [
          {
            id: 1,
            value: '测试数据'
          }
        ]
      }, 1200)
    },
    // 选中列表
    selectedItem(item) {
      if (this.isEdit) {
        this.$Modal.confirm({
          title: '提示',
          content: '您确定要退出当前编辑界面吗？',
          onOk: () => {
            this.isEdit = false;
            let id = item.id;
            this.activeItem = id;
          }
        })
        return;
      }
      let id = item.id;
      this.activeItem = id;
    },
    // 点击新增
    add_click() {
      this.activeItem = -1;
      this.isEdit = true;
    },
    // 点击编辑
    update_click() {
      this.isEdit = true;
    },
    // 点击删除
    delete_click() {
      this.$Modal.confirm({
        title: '提示',
        content: '您确定要删除吗？',
        onOk: () => {
          // 删除
        }
      })
    },
    // 点击取消
    cancel_click() {
      this.isEdit = false;
    },
    // 点击保存
    save_click() {
      this.isEdit = false;
    },
    // 添加明细数据
    add_detail() {
      let value = this.tmpText;
      this.TData.push({
        name: value
      })
      this.tmpText = '';
    },
    // 删除明细数据
    delete_detail(row) {
      let index = row._index;
      this.TData.splice(index, 1)
    }
  }
}
</script>

<style lang="less">
@import '~less/color.less';
.layout {
  display: flex;
  height: 100%;
  .layout-left {
    border: 1px solid #e4e4e4;
    height: 100%;
    flex-basis: 250px;
    display: flex;
    flex-direction: column;
    .list-search {
      flex-basis: 40px;
      margin: 10px;
    }
    .list-content {
      flex: 1;
      li {
        line-height: 35px;
        font-size: 14px;
        font-size: 700;
        color: @textColor;
        padding: 0 10px;
        margin-bottom: 5px;
        cursor: pointer;
        &:hover {
          background-color: @greyLight;
          color: @hoverTextColor;
        }
        &.list-acitve {
          background-color: @greyLight;
          color: @hoverTextColor;
        }
        .list-index {
          margin-right: 10px;
        }
      }
    }
    .list-page {
      flex-basis: 40px;
    }
  }
  .layout-right {
    height: 100%;
    flex: 1;
    padding: 0 10px;
    .layout-action {
      margin-bottom: 30px;
    }
    .add-item {
      margin-left: 3px;
    }
    .row-select {
      width: 150px;
    }
  }
}
</style>
