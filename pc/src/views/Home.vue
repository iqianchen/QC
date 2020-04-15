<template>
  <div id="home">
    <!-- 主体 -->
    <div id="outside-main">
      <!-- 左侧菜单栏 -->
      <div id="left-menu">
        <div class="line"></div>
        <div class="info">
          <span class="image"></span>
          <span class="message">用户名称</span>
        <div class="line"></div>
        </div>
        <nav-bar></nav-bar>
      </div>
      <!-- 内容区域 -->
      <div id="outside-content">
        <!-- <Spin v-if=""></Spin> -->
        <main-body></main-body>
      </div>
    </div>
  </div>
</template>

<script>
// import test from 'js/test.js'
import NavBar from '#/homeLayout/NavBar'
import MainBody from '#/homeLayout/MainBody'

export default {
  name: 'home',
  components: {
    NavBar,
    MainBody
  },
  mounted() {
    // test.start()

    // setTimeout(() => {
    //   test.close()
    // }, 3000)
  }
}
</script>

<style lang="less">
@import '~less/color.less';

#home {
  height: 100%;
  width: 100%;
  #outside-main {
    height: 100%;
    display: flex;

    #left-menu {
      flex-basis: 220px;
      box-sizing: border-box;
      height: 100%;
      background-color: @navBgColor;
      padding-top: 30px;

      .line {
        display: block;
        width: 100%;
        height: 2px;
        // background-color: #3e4552;
        background-color: #6a748a;
        margin-top: 10px;
      }
      .info {
        // margin: 20px 0px;
        // text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
        // height: 50px;
        &::after,
        &::before {
          content: '';
          display: block;
          width: 100%;
          height: 1px;
          // background-color: #6a748a;
          background-color: #2a303c;
        }

        .image {
          display: inline-block;
          width: 80px;
          height: 80px;
          margin: 15px 0;
          border: 1px solid #e4e4e4;
          border-radius: 50%;
        }

        .message {
          color: #fff;
        }
      }
    }

    #outside-content {
      height: 100%;
      box-sizing: border-box;
      overflow: hidden;
      flex:1;
    }
  }
}
</style>