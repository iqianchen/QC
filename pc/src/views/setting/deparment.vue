<template>
  <div id="deparment">
    <SimpleTable
      :columns="columns"
      :option="option"
      ref="simpleTable"
      @deleteRow="deleteRow"
      @submit="submit"
      @addClick="add_click">

      <div slot="detailPage">
        <div class="row">
          <span class="label">供应商</span>
          <Input v-model="data.name" />
        </div>
        <div class="row">
          <span class="label">检验方式</span>
          <Select v-model="data.typeId">
            <Option v-for="item in typeList" :key="item.id" :value="item.id">{{ item.name }}</Option>
          </Select>
        </div>
        <div class="row" v-if="data.typeId == 2">
          <span class="label">抽查比例</span>
          <Input v-model="data.rate" />
        </div>

        <div class="group">
          <div class="group-title">选项</div>
          <div class="group-box">
            <!-- <CheckboxGroup v-model="data.promission"> -->
              <Checkbox label="data.isResult">检验后直接产生检验单</Checkbox>
              <Checkbox label="data.appeal">是否需要审核</Checkbox>
            <!-- </CheckboxGroup> -->
          </div>
        </div>
      </div>
    </SimpleTable>
  </div>
</template>

<script>
import SimpleTable from '#/SimpleTable';
export default {
  name: 'deparment',
  components: {
    SimpleTable
  },
  data() {
    return {
      columns: [
        {
          key: 'supplier',
          title: '供应商',
          maxWidth: 320,
          tooltip: true   // 文本将不换行，超出部分显示为省略号，并用 Tooltip 组件显示完整内容
        }, {
          key: 'testType',
          title: '检验方式',
          width: 120,
          render: (h, params) => {
            let value = '';
            switch (params.row.testType) {
              case 1:
                value = '全检';
                break;
              case 2:
                value = '抽查';
                break;
              case 3:
                value = '免检';
                break;
            }
            return h('span', {}, value)
          }
        }, {
          key: 'rate',
          width: 100,
          title: '比例'
        }, {
          key: 'enable',
          title: '是否启用',
          width: 100,
          align: 'center',
          render: (h, params) => {
            let value = false;
            if (params.row.enable) {
              value = true;
            }
            return h('Icon', {
              props: {
                type: value ? 'ios-checkmark-circle' : 'ios-close-circle',
                size: 24,
                color: value ? '#19be6b' : '#ed4014'
              }
            })
          }
        }, {
          key: 'isResult',
          width: 160,
          align: 'center',
          title: '是否直接产生检验结果',
          render: (h, params) => {
            let value = false;
            if (params.row.isResult) {
              value = true;
            }
            return h('Icon', {
              props: {
                type: value ? 'ios-checkmark-circle' : 'ios-close-circle',
                size: 24,
                color: value ? '#19be6b' : '#ed4014'
              }
            })
          }
        }
      ],
      option: {
        page: 'deparment',
        width: 600,
        icon: 'ios-filing',
        placeholder: '请输入供应商名称',
      },
      data: {
        name: '',
        typeId: 1,
        rate: 25,
        isResult: '',
        appeal: ''
      },
      typeList: [
        {
          id: 1,
          name: "全检"
        }, {
          id: 2,
          name: '抽查'
        }, {
          id: 3,
          name: '免检'
        }
      ]
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