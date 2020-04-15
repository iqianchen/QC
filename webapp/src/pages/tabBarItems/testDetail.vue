<template>
  <div id="testDetail">
    <div class="noData" v-if="showPage === 'noData'">
      <!-- <p>没有找到该产品，请核对产品条码是否有误</p>
      <div class="button">
        <cube-button :outline="true" @click="back">返回</cube-button>
      </div> -->
      <error :custom="true" align="top" icon="#icon-cuowu">
        <div slot="content">
          <p>没有找到该产品，请核对产品条码是否有误</p>
          <div class="button">
            <cube-button :outline="true" @click="back">返回</cube-button>
          </div>
        </div>
      </error>
    </div>
    <div class="completed" v-if="showPage === 'completed'">
      <error :icon="result ? '#icon-chenggong': '#icon-cuowu'" :custom="true" align="top">
        <div slot="content">
          <p v-text="result ? '该产品已检验合格':'该产品检验不合格'"></p>
          <div class="button">
            <cube-button :outline="true" @click="viewData" v-if="result">查看详情</cube-button><br>
            <cube-button :outline="true" v-text="result ? '反审核':'再次检验'" @click="modifyData"></cube-button><br>
            <cube-button :outline="true" @click="back">返回</cube-button><br>
          </div>
        </div>
      </error>
    </div>

    <div class="detail" v-if="showPage === 'detail'">
      <div class="list">
        <ul class="list-content">
          <li class="list-item tag" v-if="actionType !== 'add'">
            <span class="label">检验员</span>：
            <span v-text="datas.userName"></span>
          </li>
          <li class="list-item tag" v-if="actionType !== 'add'">
            <span class="label">检验时间</span>：
            <span>{{datas.testTime | dateFormat}}</span>
          </li>
          <li class="list-item" v-for="(value, key) in allList" v-if="datas[key]">
            <span class="label" v-text="value"></span>：
            <span v-text="datas[key]"></span>
          </li>
        </ul>
      </div>
      <div class="testProject" v-for="item in datas.project">
        <div class="list">
          <div class="list-title">
            <svg class="iconfont" aria-hidden="true">
              <use xlink:href="#icon-chanpin"></use>
            </svg>
            <span style="margin-left:10px" v-text="item.projectName"></span>
          </div>
          <ul class="list-content">
            <li class="list-panel" v-for="(childItem, index) in item.detail">
              <div class="list-item">
                <span style="width:45px">项次{{index+1}}</span>
                <span v-text="childItem.detail"></span>
              </div>
              <div class="list-action">
                <cube-radio-group :horizontal="true" v-model="childItem.isPass">
                  <cube-radio :class="{'fail': option.value == 0}" v-for="(option, index) in options" @input="radioChange" :option="option" :key="index" v-model="childItem.isPass"></cube-radio>
                </cube-radio-group>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div class="list action">
        <div class="totalJudge" style="display: flex">
          <span>综合判定</span>
          <div>
            <cube-radio-group :horizontal="true" v-model="datas.isPass">
              <cube-radio :class="{'fail': option.value == 0}" v-for="(option, index) in options" @input="allTestResult" :key="index" :option="option" v-model="datas.isPass"></cube-radio>
            </cube-radio-group>
          </div>
        </div>
        <div class="upload">
          <div class="box" v-for="(item, index) in files" :key="index">
            <cube-upload @files-added="addedHandler" @file-error="errHandler" :action="uploadApi" v-model="item.images" :simultaneous-uploads="1" :max="1"></cube-upload>
            <span v-text="item.label"></span>
          </div>
        </div>
        <div class="list-checkbox font-samll" v-if="query.testType == 1">
          <cube-checkbox v-model="batchTest" shape="square">
            相同款式生成统一结果（只对已分配的检验任务生效）
          </cube-checkbox>
        </div>
        <div class="list-checkbox font-samll">
          <cube-checkbox v-model="orderTest" shape="square">
            对此单号产品一起判定(相同品号、款式、生产单号)
          </cube-checkbox>
        </div>
        <div class="desc">
          <span class="label">描述：</span>
          <div>
            <cube-textarea v-model="datas.desc" placeholder="请输入对检验结果的描述" :maxlength="100" :readonly="actionType == 'see'"></cube-textarea>
          </div>
        </div>

        <cube-button v-if="actionType !== 'see'" @click="submit">结果上传</cube-button>
      </div>
    </div>
  </div>
</template>

<script>
import Setting from '@/config/Setting.js'
import initMixin from '@/mixin/init.js'
// import { setTimeout } from 'timers';
import error from '#/error'
export default {
  name: 'testDetail',
  mixins: [initMixin],
  components: {
    error
  },
  data() {
    return {
      datas: {},
      query: {},
      batchTest: false,
      orderTest: false,
      showPage: false,
      result: null,
      actionType: 'add',
      loading: false,
      options: [
        {
          label: '合格',
          value: 1
        },{
          label: '不合格',
          value: 0
        }
      ],
      allList: {
        supplierName: '供应商',
        barCode: '条码',
        purNo: '生产单号',
        styleCode: '产品型号',
        fetchSize: '面料编号',
        goodsSpec: '产品规格',
        size: '产品尺寸',
        clrName: '外架颜色',
        rmQLTName: '主要材质'
      },
      files: [  // 在images可以设置默认图片
        { label: '合格证+底标照', images: [] },
        { label: '产品整套正面照', images: [] },
        { label: '产品整套背面', images: [] }
      ],  
      uploadApi: Setting.baseURL + '/zyTest/uploadImg'
    }
  },
  mounted() {
    let query = this.$route.query
    this.query = query
    this.getData(query.barCode)
  },
  methods: {
    // 通过条码获取数据
    async getData(barCode) {
      let url = 'zyTest/getTestProject?barCode=' + barCode
      let result = await this.$http.get(url)
      if (!result.data) {
        this.showPage = 'noData'
        return;
      }
      let datas = result.data
      if (result.testResult) {
        switch (result.testResult) {
          case 1: // 未检验
            this.showPage = 'detail'
            break;
          case 2: // 检验合格
            datas = this._hanleData(datas)
            this.showPage = 'completed'
            this.result = true
            break;
          case 3: // 检验不合格
            datas = this._hanleData(datas)
            this.showPage = 'completed'
            this.result = false
            break;
          default: // 数据不存在
            this.showPage = 'noData'
            datas = []
        }
      }
      this.datas = datas
    },
    // 处理数据
    _hanleData(datas) {
      datas.project.forEach(item => {
        item.detail.forEach( value => {
          value.isPass = value.isPass ? 1 : 0
        })
      })
      datas.isPass = datas.isPass ? 1 : 0
      this.files[0].images = [{url: datas.image1}]
      this.files[1].images = [{url: datas.image2}]
      this.files[2].images = [{url: datas.image3}]
      return datas;
    },
    // 图片上传成功
    addedHandler(event) {
      // console.log('event', event)
    },
    // 图片上传失败
    errHandler(err) {
      // console.log('err', err)
      // Alias /testWebapp "c:/Users/songdb/Desktop/songdb/ZYTest/webapp"
      // <Directory "c:/Users/songdb/Desktop/songdb/ZYTest/webapp">
      // Options Indexes FollowSymLinks
      // AllowOverride None
      // Require all granted
      // </Directory>
    },
    // 单选框值改变
    radioChange() {
      let project = this.datas.project
      let isPass;
      let selectedAll = true
      if (project) {
        for (let i=0;i<project.length;i++) {
          let detail = project[i].detail
          for (let j=0;j<detail.length;j++) {
            if (detail[j].isPass === 0) {
              this.datas.isPass = 0
              return
            }else if(!detail[j].isPass) {
              // return
              selectedAll = false
              continue
            }
          }
        }
        if (selectedAll) this.datas.isPass = 1
      }
    },
    // 综合判定
    allTestResult(value) {
      let project = this.datas.project
      if (value === 1 && project) {
        for (let i=0;i<project.length;i++) {
          let detail = project[i].detail
          for (let j=0;j<detail.length;j++) {
            if (detail[j].isPass === 0) {
              this.datas.isPass = 0
              this._showToast('有不合格的项次，请检查')
              return;
            }
          }
        }
      }
    },
    // 提交
    async submit() {
      // if (this.loading) return;  // 不能重复提交
      this.loading = true
      let newData = {...this.datas}
      // 获取图片
      for (let i=0;i<this.files.length;i++) {
        if (this.files[i].images.length == 0) {
          this._showToast('还有图片未上传')
          return
        }
        if (this.files[i].images[0].response) {
          newData[`image${i+1}`] = Setting.ImgUrl + this.files[i].images[0].response.data.relativePath
        }
      }
      // newData.project.forEach(item => {
      //   item.detail.forEach( value => {
      //     if (value.isPass === 1) value.isPass = true
      //     if (value.isPass === 0) value.isPass = false
      //   })
      // })
      // if (newData.isPass === 1) newData.isPass = true
      // else if (newData.isPass === 0) newData.isPass = false
      // else {
      // }
      if (!newData.isPass && newData.isPass !== 0) {
        this._showToast('还未进行综合判定')
        return
      }
      newData.project = JSON.stringify(newData.project)
      let params = Object.assign(newData, {
        userId: this.$global.userInfo.userId || 'manager5843',
        testId: this.query.testId,
        testType: this.query.testType,
      })
      if (this.query.type == 1) {
        params.batchTest = this.batchTest
      }
      params.orderTest = this.orderTest

      // console.log('params', params)
      // return;

      try {
        let result = await this.$http.post('/zyTest/addTest', params)
        this._showToast('上传成功', 'correct')
        setTimeout(()=>{
          this.back()
          this.loading = false
        },600)
      } catch (e) {
        this._showToast(`上传失败: ${e}`, 'error')
      }
    },
    // 轻提示
    _showToast(msg, type = 'txt') {
      this.toast = this.$createToast({
        txt: msg,
        type: type
      })
      this.toast.show()
    },
    // 查看数据
    viewData() {
      this.actionType = 'see'
      this.showPage = 'detail'
    },
    // 修改数据
    modifyData() {
      this.actionType = 'modify'
      this.showPage = 'detail'
    },
    back() {
      this.$router.push({
        path: '/home',
        query: {
          type: this.query.type,
        }
      })
    }
  }
}
</script>

<style lang="less">
@import '~less/color.less';
#testDetail {
  background-color: @greyShadow;
  .detail {
    padding: 5px 0;
  }
  .list-panel {
    position: relative;
    padding-top: 6px;
    // border-bottom: 1px solid @border;
    border-bottom: 1px solid @greenLight;
    &:last-child {
      border-bottom: none;
    }
    .list-action {
      margin-left: 100px;
    }
  }
  .action {
    padding: 5px 15px 15px;
    color: @content;
    .totalJudge {
      display: flex;
      align-items: center;
      >span {
        flex: 1
      }
      >div {
        flex: 2
      }
    }
    .upload {
      display: flex;
      justify-content: space-between;
      .box {
        font-size: 14px;
        display: flex;
        flex-direction: column;
        align-items: center;
      }
    }
    .desc {
      margin: 10px 0 15px;
      display: flex;
      .label {
        font-size: 14px;
        display: inline-block;
      }
      >div {
        flex: 1;
      }
    }
  }

  .noData,
  .completed {
    // padding-top: 30px;
    height: 100%;
    background-color: #fff;
    text-align: center;
    p {
      text-align: center;
      color: @title;
      font-size: 16px;
      font-weight: 700;
      margin: 20px 0 30px;
    }
    .button {
      width: 70%;
      margin:0 auto;
    }
  }
}

#testDetail .cube-radio-group[data-horz=true]:after {
  border: none !important;
}
#testDetail .border-right-1px:after {
  border: none !important;
}
#testDetail .button .cube-btn:after {
  border: none;
}
#testDetail .button .cube-btn {
  border: 1px solid @orange;
  color: @orange
}
#testDetail .cube-radio_selected .cube-radio-ui {
  background-color: @green;
}
#testDetail .fail.cube-radio_selected .cube-radio-ui {
  background-color: @red;
}
#testDetail .detail .cube-btn {
  background: @gradualBlue;
}
#testDetail .cube-checkbox_checked .cube-checkbox-ui i {
  color: @green;
}
#testDetail .list-checkbox .cube-checkbox {
  padding: 0 3px;
  font-size: 12px;
}
</style>

