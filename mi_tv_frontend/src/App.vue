<template>
  <NavBar></NavBar>
  <RouterView />
</template>

<script lang="ts">
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
  components: {
    NavBar: NavBar,
  },
});
</script>
