<template>
  <a :href="href" class="p-1 font-semibold m-4 hover:text-white"
    ><slot></slot
  ></a>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "NavItem",
  props: {
    href: {
      type: String,
      required: true,
    },
  },
});
</script>
