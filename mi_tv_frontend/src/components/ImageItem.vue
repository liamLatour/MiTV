<!-- https://css-tricks.com/lazy-loading-images-with-vue-js-directives-and-intersection-observer/ -->

<template>
  <figure v-lazyload class="h-full flex justify-center items-center">
    <font-awesome-icon
      icon="fa-solid fa-spinner"
      class="animate-spin w-10 h-10 absolute"
    />
    <img class="object-cover h-full max-w-full" :data-url="source" alt="" />
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
