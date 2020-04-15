<template>
  <div id="popupModel">
    <Modal v-model="isShow" :title="title" width="650">
      <div class="modal-search">
        <Input 
          search
          autofocus
          enter-button
          class="search-input"
          placeholder="请输入代号或名称"
          @on-search="search"
          />

        <Checkbox label="checkbox" @on-change="changeCheck">
          <span>启用多选</span>
        </Checkbox>
      </div>

      <tableModel
        :hideHeader="true"
        :columns="columns"
        :options="options"
        ref="tableModel">
      </tableModel>
    </Modal>
  </div>
</template>

<script>
import tableModel from '#/tableModel';
export default {
  name: 'popupModel',
  components: {
    tableModel
  },
  data() {
    return {
      isShow: false,
      title: '标题',

      columns: [{
        title: '经销商代号',
        key: 'resellerCode',
        width: 120,
        align: 'center'
      },{
        title: '经销商名称',
        key: 'resellerName',
        align: 'center',
        tooltip: true
      }],
      options: {
        url: '/goods/getAllReseller',
        selection: false,
        pageSize: 10,
        height: 400
      }   
    }
  },

  methods: {
    show() {
      this.isShow = true;
    },
    changeCheck(value) {
      this.options.selection = value
    },
    search(keyWord) {
      this.$refs.tableModel.getData({
        keyWord: keyWord
      })
    }
  }
}
</script>

<style lang="less">
.modal-search {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  .search-input {
    margin-right: 20px;
    width: 300px;
  }
}
</style>
