<template>
  <div class="loading-bg">
    <div class="loading-content">
      <span class="loading-icon"></span>
      <span class="loading-text" v-if="text"></span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: ''
    }
  }
}
</script>

<style lang="less">
.loading-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255,255,255,.7);

  .loading-content {
    position: absolute;
    display: block;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    text-align: center;
    .loading-icon {
      display: block;
      width: 35px;
      height: 35px;
      border-radius: 50%;
      background-color: #2d8cf0;
      animation: loading-animation 1.1s 0s ease-in-out infinite;
    }
    .loading-text {
      display: inline-block;
      margin-top: 8px;
      color: #2d8cf0;
      font-size: 16px;
    }
  }
}

@keyframes loading-animation {
  0% {
    -webkit-transform: scale(0);
    transform: scale(0)
  }
  to {
      -webkit-transform: scale(1);
      transform: scale(1);
      opacity: 0
  }
}
</style>
