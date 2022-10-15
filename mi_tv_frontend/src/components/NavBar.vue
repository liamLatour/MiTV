<template>
  <div
    class="fixed z-20 bg-gray-900 top-0 w-72 sm:visible sm:w-full sm:h-16"
    :class="{ invisible: visible }"
  >
    <div
      class="flex flex-col sm:flex-row m-auto items-center justify-between max-w-5xl h-full"
    >
      <NavItem href="/#"> Dernières photos </NavItem>
      <NavItem href="/#team"> L'équipe </NavItem>
      <NavItem href="/" class="text-xl"> MiTV </NavItem>
      <NavItem href="/#hardware"> Le matériel </NavItem>
      <NavItem href="/#legal"> Mentions légales </NavItem>
    </div>
  </div>

  <span
    class="fixed top-0 left-0 z-20 text-2xl bg-opacity-50 bg-black p-2 sm:invisible"
    @click="showNavBar"
  >
    <font-awesome-icon icon="fa-solid fa-bars" class="w-6" />
  </span>
</template>

<script lang="ts">
import NavItem from "./NavItem.vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "NavBar",
  components: {
    NavItem: NavItem,
  },
  data() {
    return {
      visible: true,
    };
  },
  methods: {
    showNavBar() {
      console.log("hey");
      this.visible = !this.visible;
    },
  },
});
</script>
