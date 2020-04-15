<template>
  <div id="error" :class="align">
    <div>
      <div v-if="icon" class="error-icon">
        <svg class="iconfont" aria-hidden="true">
          <use :xlink:href="icon"></use>
        </svg>
      </div>
      <div class="error-content">
        <slot v-if="custom" name="content"></slot>
        <p v-else v-text="message"></p>
    </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'error',
  props: {
    message: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: ''
    },
    custom: {
      type: Boolean,
      default: false
    },
    align: {
      type: String,
      default: 'center'
    }
  }
}
</script>

<style lang="less" scoped>
@import '~less/color.less';
#error {
  height: 100%;
  box-sizing: border-box;
  >div {
    .error-icon {
      font-size: 110px;
      text-align: center;
    }
    .error-content {
      color: @content;
      text-align: center;
    }
  }
  &.center {
    display: flex;
    align-items: center;
    justify-content: center;
    >div {
      transform: translateY(-50%);
    }
  }
  &.top {
    padding-top: 40px;
  }
}
</style>
