<template>
  <div class="text-center rounded bg-neutral-900 m-1 p-3 sm:w-52 sm:p-5 sm:m-5">
    <h2 class="font-semibold mb-2">{{ name }}</h2>
    <h3 class="">{{ type }}</h3>
    <h4 class="mt-2 text-gray-500">{{ reference }}</h4>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "PhotoGear",
  props: {
    type: {
      type: String,
    },
    name: {
      type: String,
    },
    reference: {
      type: String,
    },
  },
});
</script>
