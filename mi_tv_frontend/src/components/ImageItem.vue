<template>
  <figure v-lazyload class="image__wrapper">
    <img class="image__item" :data-url="source" alt="random image" />
  </figure>
</template>

<script lang="ts">
export default {
  name: "ImageItem",
  props: {
    source: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped lang="scss">
.image__wrapper {
  .image__item {
    object-fit: cover;
    height: 100%;
    width: 100%;
  }
}
</style>
