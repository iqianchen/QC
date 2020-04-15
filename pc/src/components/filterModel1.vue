<template>
  <!-- 条件过滤模型 -->
  <div id="filterModel">
    <div>
      <div class="filter-item" v-for="item in filter" :key="item.key">
        <!-- 文本类型 -->
        <div class="text" v-if="item.type ==='text' || !item.type">
          <span class="label" v-text="item.label"></span>
          <Input 
            clearable 
            v-model="item.value" 
            :placeholder="item.placeholder" />
        </div>
        <!-- 弹出框类型 -->
        <div class="popup" v-else-if="item.type === 'popup'">
          <Button
            type="primary"
            icon="ios-add-circle-outline"
            @click="showModel(item.key)">
            {{item.label}}
          </Button>
          <Input
            clearable
            readonly
            v-model="item.value"
            :placeholder="item.placeholder"
            @on-change="item.value = ''" />
        </div>
        <!-- 日期类型 -->
        <div class="date" v-else-if="item.type === 'date'">
          <span class="label" v-text="item.label"></span>
          <DatePicker 
            type="daterange"
            format="yyyy-MM-dd"
            split-panels
            :placeholder="item.placeholder">
          </DatePicker>
        </div>
        <!-- 下拉框类型 -->
        <div class="select" v-else-if="item.type == 'select'">
          <span class="label" v-text="item.label"></span>
          <Select v-model="item.value" :placeholder="item.placeholder">
            <Option
              v-for="subItem in item.data"
              :value="subItem.value"
              :key="subItem.value">
              {{ subItem.text }}
            </Option>
          </Select>
        </div>
        <!-- 单选框类型 -->
        <div class="radio" v-else-if="item.type === 'radio'">
          <RadioGroup v-model="item.value">
            <Radio 
              v-for="subItem in item.data"
              :label="subItem.text"
              :key="subItem.value"
              :value="subItem.value">
            </Radio>
          </RadioGroup>
        </div>
      </div>
    </div>

    <Button class="search" icon="ios-search" @click="search">搜索</Button>
    <popupModel ref="popupModel"></popupModel>
  </div>
</template>

<script>
import popupModel from '#/popupModel'
export default {
  components: {
    popupModel
  },
  data() {
    return {
      popupShow: false
    }
  },
  props: {
    filter: {
      type: Array,
      default() {
        return []
      }
    }
  },
  methods: {
    showModel() {
      this.$refs.popupModel.show()
    },
    // 点击搜索  传递搜索事件 并传递参数
    search() {
      if (this.filter.length === 0) return;
      let params = {};
      this.filter.map(item => {
        Object.assign(params, {
          [item.key]: item.value
        })
      })
      this.$emit('search', params)
    }
  }
}
</script>

<style lang="less">
#filterModel {
  position: relative;
  display: flex;
  >div:first-child {
    flex: 1
  }
  .filter-item {
    // display: block;
    display: inline-block;
    >div {
      width: 200px;
      display: flex;
      align-items: center;
      .label {
        flex-basis: 60px;
        text-align: right;
        padding-right: 7px;
      }
      >div {
        flex: 1
      }
    }
  }

  .search {
    flex-basis: 110px;
    text-align: center;
  }
}
</style>
