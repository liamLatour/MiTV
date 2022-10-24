<template>
  <router-link
    :to="href"
    v-scroll-to="scroll_to"
    class="p-1 pl-2 pr-2 font-medium m-4 rounded-3xl text-gray-300 hover:text-cyan-200"
  >
    <slot></slot>
  </router-link>
</template>

<script lang="ts">
import { RouterLink } from "vue-router";
import { defineComponent } from "vue";

export default defineComponent({
  name: "NavItem",
  components: {
    RouterLink: RouterLink,
  },
  props: {
    href: {
      type: String,
      required: true,
    },
    scroll_to: {
      type: String,
      default: "",
    },
  },
});
</script>
