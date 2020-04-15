<template>
  <div id="home">
    <div v-if="showPage" class="content">
      <cube-tab-panels v-model="selectedLabel">
        <cube-tab-panel v-for="item in tabs" :label="item.label" :key="item.label">
          <!-- <component :is="item.component"></component> -->
          <test v-if="item.label === '检验'" :dd="dd"></test>
          <task v-if="item.label === '任务'" @taskNum="taskNum"></task>
          <notice v-if="item.label === '通知'"></notice>
        </cube-tab-panel>
      </cube-tab-panels>
    </div>
    <div v-if="showPage" class="tabBar">
      <cube-tab-bar v-model="selectedLabel">
        <cube-tab v-for="item in tabs" :label="item.label" :key="item.label">
            <span slot="icon" style="position: relative; width: 1.5em; height: 1.5em">
              <span class="badge" v-if="item.badge && !isNaN(item.badge)">
                <i v-if="item.badge > 0 && item.badge < 100" :class="{complex: item.badge >= 10 }" v-text="item.badge"></i>
                <i v-else-if="item.badge > 100" class="more">99+</i>
              </span>
              <svg class="iconfont tabicon" aria-hidden="true">
                <use :xlink:href="item.icon"></use>
              </svg>
            </span>
        </cube-tab>
      </cube-tab-bar>
    </div>
    <error v-if="nologin" icon="#icon-cuowu" align="center" message="您还不是管理员或检验员"></error>
    <loading v-if="!showPage"></loading>
  </div>
</template>

<script>
import Setting from '@/config/Setting.js'
import notice from 'p/tabBarItems/notice'
import task from 'p/tabBarItems/task'
import test from 'p/tabBarItems/test'
import loading from '#/loading'
import error from '#/error'

export default {
  name: 'home',
  components: {
    notice,
    task,
    test,
    loading,
    error
  },
  data() {
    return {
      showPage: false,
      nologin: false,
      selectedLabel: '检验',
      tabs: [
        {
          label: '检验',
          icon: '#icon-saomaxiche-',
          component: test
        },{
          label: '任务',
          badge: 0,
          icon: '#icon-renwu',
          component: task
        },{
          label: '通知',
          icon: '#icon-tongzhi',
          component: notice
        }
      ]
    }
  },
  mounted() {
    setTimeout(()=>{
      this._login()
    },500)
    this._switchTab()
  },
  methods: {
    _login() {
      let _this = this
      if (dd && !_this.$global.userInfo) {
        dd.ready(function(){
          // 获取免登授权码
          dd.runtime.permission.requestAuthCode({
            corpId: Setting.corpId,
            onSuccess: function(result) {
              let url = '/user/getUserInfo?code=' + result.code
              _this.$http.get(url).then(res => {
                if (res) {
                  // 保存用户信息
                  _this.$global.setUserInfo(res)
                  dd.biz.navigation.setTitle({title: '部门通知'})
                  _this.showPage = true
                } else {
                  _this.nologin = true
                }
              })
            }
          })
        })
      } else if (_this.$global.userInfo) {
        _this.showPage = true
      }

      // 1905311002503
      // _this.$global.setUserInfo({
      //   // userId: 'manager5843'
      //   userId: '210543183923306624'
      // })
      // _this.showPage = true
    },
    taskNum(num) {
      this.tabs[1].badge = num
    },
    _switchTab() {
      let query = this.$route.query
      if (query && query.type) {
        switch(query.type) {
          case "0":
            this.selectedLabel = '检验';
            // dd.biz.navigation.setTitle({title: '产品检验'})
            break;
          case "1":
            this.selectedLabel = '任务';
            // dd.biz.navigation.setTitle({title: '检验任务'})
            break;
        }
      }
    },
  }
}
</script>

<style lang="less">
@import '~less/color.less';
#home {
  height: 100%;

  .tabBar {
    height: 50px;
    box-sizing: border-box;
    .tabicon {
      width: 1.5em;
      height: 1.5em;
    }
  }
  .content {
    height: calc(100% - 50px);
    background: @greyShadow;
  }

  .cube-tab-panels {
    height: 100%;
  }
  .badge {
    font-size: 12px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: @red;
    text-align: center;
    line-height: 16px;
    color: @white;
    position: absolute;
    right: -7px;
    top: -10px;
    >i {
      font-style: normal;
      display: block;
      transform: scale(0.9);
      &.complex {
        transform: scale(0.8)
      }
      &.more {
        transform: scale(0.7)
      }
    }
  }
}

#home .cube-tab-panels-group {
  height: 100%;
}
#home .cube-tab {
  padding: 4px 0;
}
#home .cube-tab>div {
  font-size: 14px;
  margin-top: 3px;
}
#home .before-trigger span {
  color: @help;
}
</style>


