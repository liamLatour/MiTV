<template>
  <NavBar />
  <RouterView />
</template>

<script lang="ts">
import NavBar from "./components/NavBar.vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
  components: {
    NavBar: NavBar,
  },
});
</script>
