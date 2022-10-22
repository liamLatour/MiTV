<template>
  <router-link :to="href" class="p-1 font-semibold m-4 hover:text-white">
    <slot></slot>
  </router-link>
</template>

<script lang="ts">
import { RouterLink, RouterView } from "vue-router";
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
  },
});
</script>
