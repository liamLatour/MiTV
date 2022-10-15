<template>
  <div
    class="fixed z-10 bg-gray-900 top-0 w-72 sm:visible sm:w-full sm:h-16"
    :class="{ invisible: visible }"
  >
    <div
      class="flex flex-col sm:flex-row m-auto items-center justify-between max-w-5xl h-full"
    >
      <NavItem href="/#legal"> Dernières photos </NavItem>
      <NavItem href="/#team"> L'équipe </NavItem>
      <NavItem href="/#legal" class="text-xl"> MiTV </NavItem>
      <NavItem href="/#legal"> Le matériel </NavItem>
      <NavItem href="/#legal"> Mentions légales </NavItem>
    </div>
  </div>

  <span
    class="fixed top-0 left-0 z-10 text-2xl bg-opacity-50 bg-black p-3 sm:invisible"
    @click="showNavBar"
  >
    <font-awesome-icon icon="fa-solid fa-bars" />
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
