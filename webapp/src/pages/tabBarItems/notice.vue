<template>
  <div id="notice" :style="{height: scrollHeight}">
    <cube-scroll ref="scroll" :data="datas" :options="options" @pulling-down="onPullingDown" @pulling-up="onPullingUp">
      <div class="card" v-for="(item, index) in datas">
        <div class="card-item" @click="showDetail(item.id)">
          <div v-if="item.src" class="image">
            <img :src="item.src" alt="">
          </div>
          <div v-if="item.updateDate" class="message font-mini">{{item.updateDate | dateFormat}}</div>
          <div class="text-content indent font-samll" v-text="item.content"></div>
        </div>
      </div>
    </cube-scroll>
  </div>
</template>

<script>
import initMixin from '@/mixin/init.js'

export default {
  name: 'notice',
  mixins: [initMixin],
  data() {
    return {
      datas: [],
      pageOptions: {
        pageIndex: 1,
        pageSize: 10
      },
      scrollbar: false,
      startY: 0,
      scrollHeight: 0
    }
  },
  computed: {
    options() {
      return {
        startY: this.startY,
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
  created() {
    this.getNotice()
  },
  mounted() {
    this.initPage()
  },
  methods: {
    initPage() {
      this.scrollHeight = window.innerHeight - 50 + 'px'
      setTimeout(() => {
        this.$refs.scroll.refresh()
      }, 30);
    },
    // 获取消息通知
    async getNotice() {
      let result = await this.$http.post('/project/getAllNotice', this.pageOptions)
      this.datas = this.datas.concat(result.data)
    },
    // 下拉刷新
    onPullingDown() {
      this.pageOptions.pageIndex = 1
      this.datas = []
      this.getNotice()
      this.$refs.scroll.forceUpdate()
    },
    // 上拉加载
    onPullingUp() {
      this.pageOptions.pageIndex++
      this.getNotice()
      this.$refs.scroll.forceUpdate()
    },
    showDetail(id) {
      // this.$router.push('/notice/detail/' + id)
    }
  }
}
</script>


