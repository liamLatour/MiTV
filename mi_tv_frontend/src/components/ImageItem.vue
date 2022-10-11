<!-- https://css-tricks.com/lazy-loading-images-with-vue-js-directives-and-intersection-observer/ -->

<template>
  <figure v-lazyload class="image__wrapper">
    <font-awesome-icon icon="fa-solid fa-spinner" />
    <img class="image__item" :data-url="source" alt="" />
  </figure>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "ImageItem",
  props: {
    source: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped lang="scss">
.image__wrapper {
  height: 100%;
  .image__item {
    object-fit: cover;
    height: 100%;
    width: 100%;
  }
}

@keyframes spinner {
  to {
    transform: rotate(360deg);
  }
}
.fa-spinner {
  animation: spinner 1s linear infinite;
  position: absolute;
  width: 40px;
  height: 40px;
  left: calc(50% - 20px);
  top: calc(50% - 20px);
}
</style>
