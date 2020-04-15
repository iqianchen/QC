<template>
  <div id="test">
    <div class="message">
      温馨提示：请优先完成检验任务
    </div>
    <cube-button @click="startTest" icon="cubeic-scan">
      开始检验
    </cube-button>
  </div>
</template>

<script>
export default {
  name: 'test',
  methods: {
    startTest() {
      let _this = this
      if (dd) {
        dd.biz.util.scan({
          tips: '产品检验',
          onSuccess: function(res) {
            var barCode = res.text
            _this.$router.push({
              path: '/test/testDetail',
              query: {
                testType: 0,
                barCode: barCode
              }
            })
          }
        })
      }
    }
  }
}
</script>

<style lang="less">
@import "~less/color.less";
#test .cube-btn {
  // background: @gradualGreen;
  background: @gradualBlue;
  width: 60%;
  margin: 200px auto;
}
#test .message {
  color: @help;
  font-size:12px;
  text-align: center;
  margin-top: 30px;
}
</style>
