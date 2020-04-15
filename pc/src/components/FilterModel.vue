<template>
  <div id="filterModel">
    <div class="row" :class="item._isError ? 'error': ''" v-for="item in filter" :key="item.key">
      <span class="label" :class="item.require ? 'require':''" v-text="item.label"></span>
      <!-- 文本类型 -->
      <div class="text" v-if="item.type === 'text'">
        <Input size="small" v-model="item.value"  :placeholder="item.placeholder" @on-blur="textBlur(item)"/>
      </div>

      <!-- 日期类型 -->
      <div class="date-group" v-else-if="item.type === 'date'">
        <DatePicker 
          class="date-picker" 
          type="date"
          size="small"
          :value="item.value[0] || ''" 
          placeholder="开始日期" 
          @on-change="changeDate($event,item,'start')">
        </DatePicker>
        <span class="line"></span>
        <DatePicker 
          class="date-picker" 
          type="date"
          size="small"
          :value="item.value[1] || ''" 
          placeholder="结束日期"
          @on-change="changeDate($event,item,'end')">
        </DatePicker>
      </div>

      <!-- 单选框类型 -->
      <div class="radio-group" v-else-if="item.type === 'radio'">
        <RadioGroup v-model="item.value">
          <Radio v-for="subItem in item.data" :key="subItem.value" :label="subItem.value">{{subItem.text}}</Radio>
        </RadioGroup>
      </div>
      <span class="error-message" v-text="item._errorMessage"></span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filter: []
    }
  },
  props: {
    params: {
      type: Array,
      default() {
        return []
      }
    }
  },
  mounted() {
    this._initFilter();
  },
  methods: {
    // 初始化过滤参数
    _initFilter() {
      // 创建一个副本
      let tmpParams = this.params.slice();
      // 设置默认值
      let defaultValue = {
        type: 'text',
        require: false,
        _errorMessage: false,
        _isError: false
      }
      let tmpFilter = tmpParams.map(item => {
        if(item.type === 'date') {
          item.value = new Array(2)
        }
        return Object.assign({}, defaultValue, item)
      })

      this.filter = tmpFilter;
    },
    // 文本框验证
    textBlur(item) {
      if (item.require) {   // 判断是否是必须
        if (item.value) {
          item._isError = false;
          item._errorMessage = '';
        } else {
          item._isError = true;
          item._errorMessage = `${item.label}不能为空`;
        }
      }
      if (item.verification) {    // 如果需要验证则调用验证方法
        let result = item.verification(item.value)
        if (result && typeof(result) == 'string') {
          item._isError = true;
          item._errorMessage = result;
        } else {
          item._isError = false;
          item._errorMessage = '';
        }
      }
    },
    // 改变日期
    changeDate(date,item,type) {
      if (type === 'start') {
        item.value[0] = date;
      } else if (type === 'end'){
        item.value[1] = date;
      }

      if (item.value[0] && item.value[1] && new Date(item.value[0]) > new Date(item.value[1])) {
        item._isError = true;
        item._errorMessage = '开始时间不能大于结束时间';
      } else {
        item._isError = false;
        item._errorMessage = '';
      }
    },
    // 获取检验结果
    getVerifiResult() {
      let result = true;
      this.filter.map(item => {
        if (item._isError === true) result = false
      })
      return result;
    },
    // 获取筛选条件
    getFilterParam() {
      let result = this.getVerifiResult();
      if (!result) return;

      let params = {};
      this.filter.map(item => {
        params[item.key] = item.value;
      })
      return params;
    }
  }
}
</script>