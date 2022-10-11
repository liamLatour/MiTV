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
