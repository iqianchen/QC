<template>
  <div id="user">
    <SimpleTable
      :columns="columns"
      :option="option"
      ref="simpleTable"
      @deleteRow="deleteRow"
      @submit="submit"
      @addClick="add_click">

      <div slot="detailPage">
        <div class="row">
          <span class="label">用户</span>
          <Input v-model="data.userName" />
        </div>
        <div class="row">
          <span class="label">角色</span>
          <Select v-model="data.postValue">
            <Option v-for="item in postList" :key="item.value" :value="item.value">{{ item.name }}</Option>
          </Select>
        </div>

        <div class="group">
          <div class="group-title">权限</div>
          <div class="group-box">
            <CheckboxGroup v-model="data.promission">
              <Checkbox label="value1">报表查看</Checkbox>
              <Checkbox label="value2">检验单反审</Checkbox>
              <Checkbox label="value3">打印条码</Checkbox>
              <Checkbox label="value4">供应商设置</Checkbox>
              <Checkbox label="value5">检验项目设置</Checkbox>
              <Checkbox label="value7">用户设置</Checkbox>
              <Checkbox label="value6">部门通知设置</Checkbox>
              <Checkbox label="value8">检验单产生采购收货单/成品入库单</Checkbox>
              <Checkbox label="value9">审核检验单</Checkbox>
              <Checkbox label="value10">审核自动产生入库/收货检验单</Checkbox>
            </CheckboxGroup>
          </div>
        </div>
      </div>
    </SimpleTable>
  </div>
</template>

<script>
import SimpleTable from '#/SimpleTable'; 
export default {
  name: 'user',
  components: {
    SimpleTable
  },
  data() {
    return {
      data: {
        userName: '',
        postValue: '',
        promission: []
      },
      option: {
        page: 'user',
        width: 600,
        icon: 'md-person',
        placeholder: '请输入用户名称',
      },
      columns: [
        {
          key: 'name',
          width: 200,
          title: '用户名'
        },{
          key: 'number',
          width: 200,
          title: '工号'
        },{
          key: 'post',
          width: 200,
          title: '岗位',
          render: (h, params) => {
            let value = '';
            switch (params.row.post) {
              case 1:
                value = '检验员';
                break;
              case 2:
                value = '检验主管';
                break;
              case 3:
                value = '检验经理';
                break;
            }
            return h('span', {}, value)
          }
        }
      ],
      postList: [
        {
          value: 1,
          name: '检验员'
        }, {
          value: 2,
          name: '检验主管'
        }, {
          value: 3,
          name: '检验经理'
        }
      ],
    }
  },
  methods: {
    // 删除行
    deleteRow(row) {
      console.log('row', row)
      this.$refs.simpleTable.refresh()
    },
    add_click() {
      this.data = {
        userName: ''
      }
    },
    submit() {
      let editorHtml = this.editor.txt.html()
      let escapeHtml = escape(editorHtml)   // 对富文本内容进行转码转码
      this.data.content = escapeHtml
    }
  }
}
</script>