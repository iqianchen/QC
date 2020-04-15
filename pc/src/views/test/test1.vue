<template>
  <div>
    <TableModel 
      :columns="columns" 
      :action="action"
      :options="options"
      ref="tableModel"
      @filter_click="showModal = true"
    >
      <span slot="message" class="message">（默认取当月份的数据）</span>
    </TableModel>

    <Modal v-model="showModal" title="筛选" :mask-closable="false" :width="600" @on-ok="search">
      <FilterModel ref="filterModel" :params="filter"></FilterModel>
    </Modal>
  </div>
</template>

<script>
import FilterModel from '#/FilterModel';
import TableModel from '#/TableModel';
export default {
  components: {
    FilterModel,
    TableModel
  },
  data() {
    return {
      params: {
        orderDate1: '',
        orderDate2: '',
        type: '',
        proDate1: '',
        propDate2: ''
      },
      showModal: false,
      columns: [
        {
          title: '条码',
          key: 'barCode',
          width: 130,
        },{
          title: '供应商代号',
          key: 'supplierCode',
          width: 130,
        },{
          title: '供应商名称',
          key: 'supplierName',
          width: 250,
        },{
          title: '采购单号',
          key: 'purchaseCode',
          width: 150,
        },{
          title: '生产单号',
          key: 'purNo',
          width: 140,
        },{
          title: '采购单行号',
          key: 'purchaseRow',
          width: 100,
        },{
          title: '对应销售订单号',
          key: 'orderNo',
          width: 150,
        },{
          title: '销售组合批号',
          key: 'salebindCode',
          width: 120,
        },{
          title: '产品代号',
          key: 'productCode',
          width: 140,
        },{
          title: '产品名称',
          key: 'productName',
          width: 350,
        },{
          title: '规格描述',
          key: 'sizeDesc',
          width: 140,
        },{
          title: '类货品订制批号',
          key: 'customizedCode',
          width: 150,
        },{
          title: '下单日期',
          key: 'orderDate',
          align: 'center',
          width: 110,
          render: (h, params) => {
            let value = '';
            if (params.row.orderDate) {
              value = new Date(params.row.orderDate).format('yyyy-MM-dd')
            }
            return h('span', {}, value)
          }
        },{
          title: '要求交期',
          key: 'recDate',
          align: 'center',
          width: 110,
          render: (h, params) => {
            let value = '';
            if (params.row.recDate) {
              value = new Date(params.row.recDate).format('yyyy-MM-dd')
            }
            return h('span', {}, value)
          }
        },{
          title: '下单数量',
          key: 'number',
          align: 'right',
          width: 85,
        },{
          title: '款式代号',
          key: 'styleCode',
          width: 120,
        },{
          title: '款式名称',
          key: 'styleName',
          width: 150,
        },{
          title: '系列代号',
          key: 'seriesCode',
          width: 85,
        },{
          title: '系列名称',
          key: 'seriesName',
          width: 150,
        },{
          title: '产品类别代号',
          key: 'typeCode',
          width: 110,
        },{
          title: '产品类别名称',
          key: 'typeName',
          width: 150,
        },{
          title: '材质名称',
          key: 'rmQLTName',
          width: 200,
        },{
          title: '外架油漆颜色',
          key: 'clrName',
          width: 120
        },{
          title: '尺寸',
          key: 'size',
          width: 160,
        },{
          title: '面料',
          key: 'fetchSize',
          width: 150,
        },{
          title: '规格',
          key: 'goodsSpec',
          width: 130
        },{
          title: '备注',
          key: 'remark',
          width: 250
        }
      ],
      action: ['filter','downLoad'],
      options: {
        url: '/goods/getGoodsItem',
        title: '条码档案',
        pageSize: 25,
        params: {
          orderDate: ['2019-09-01', '2019-10-15']
        },
      },
      filter: [
        {
          key: 'type',
          value: '',
          type: 'radio',
          label: '类型',
          data: [
            {
              value: 1,
              text: '自产产品'
            }, {
              value: 2,
              text: '外购产品'
            }
          ]
        }, {
          key: 'orderDate',
          type: 'date',
          value: [],
          label: '下单日期'
        }, {
          key: 'proDate',
          value: [],
          type: 'date',
          label: '采购日期'
        }, {
          key: 'barCode',
          value: '',
          label: '条码',
          placeholder: '请输入条码，多个以逗号做分隔',
        }, {
          key: 'proNo',
          value: '',
          label: '生产单号',
          placeholder: '请输入生产单号，多个以逗号做分隔'
        }
      ]
    }
  },
  mounted() {

  },
  methods: {
    search() {
      console.log('11111')
      // 获取参数
      let params = this.$refs.filterModel.getFilterParam()
      if (!params) return;
      console.log('params', params)
      // 传递参数获取数据
      this.$refs.tableModel.getData(params)
    }
  }
}
</script>

<style lang="less">
.filter {
  height: 40px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}
.message {
  font-size: 14px;
}
</style>

