<template>
  <div id="task" :style="{height: scrollHeight}">
    <cube-scroll v-if="datas.length > 0" ref="scroll" :data="datas" :options="options" @pulling-down="onPullingDown" @pulling-up="onPullingUp">
      <div class="list" v-for="item in datas" :key="item.id">
        <div class="list-title">
          <div v-text="item.productName"></div>
          <div class="subTitle" v-text="item.productCode"></div>
        </div>
        <ul class="list-content">
          <li class="list-item" v-for="(value, key) in listData">
            <span class="label" v-text="value"></span>：
            <span v-text="item[key]"></span>
          </li>
        </ul>
        <div class="list-footer font-right">
          <cube-button :inline="true" :primary="true" @click="complete(item)">去完成</cube-button>
        </div>
      </div>
    </cube-scroll>
    <error v-else message="您还没有检验任务" icon="#icon-shujutongji"></error>
  </div>
</template>

<script>
import error from '#/error'
export default {
  name: 'task',
  components: {
    error
  },
  data() {
    return {
      datas: [],
      listData: {
        supplierName: '供应商',
        // purchaseCode: '采购单号',
        purNo: '生产单号',
        barCode: '商品条码',
        styleCode: '产品型号'
      },
      pageOptions: {
        pageIndex: 1,
        pageSize: 10
      },
      scrollHeight: 0
    }
  },
  mounted() {
    this.initPage()
    this.getTask()
  },
  methods: {
    initPage() {
      this.scrollHeight = window.innerHeight - 50 + 'px'
    },
    // 获取当前用户的检验任务
    async getTask() {
      let _this = this
      let params = Object.assign(this.pageOptions, {
        // userId: 'manager5843'
        userId: this.$global.userInfo.userId
      })
      let result = await this.$http.post('/task/getTaskByUser', params)
      this.datas = this.datas.concat(result.data)
      setTimeout(() => {
        this.$refs.scroll.refresh()
      }, 30);
      this.$emit('taskNum', result.total)
    },
    // 跳转到检验详情页面
    complete(value) {
      this.$router.push({
        path: '/test/testDetail',
        query: {
          barCode: value.barCode,
          testId: value.id,
          testType: 1,
        }
      })
    },
    // 下拉刷新
    onPullingDown() {
      this.pageOptions.pageIndex = 1
      this.datas = []
      this.getTask()
      this.$refs.scroll.forceUpdate()
    },
    // 上拉加载
    onPullingUp() {
      this.pageOptions.pageIndex++
      this.getTask()
      this.$refs.scroll.forceUpdate()
    },
  },
  computed: {
    options() {
      return {
        startY: 0,
        pullDownRefresh: {
          txt: '数据已更新'
        },
        pullUpLoad: {
          txt: {
            more: '正在加载...',
            noMore: '已经没有了'
          }
        }
      }
    }
  },
}
</script>