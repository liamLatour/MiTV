<template>
  <div
    class="fixed flex z-20 bg-gray-900 top-0 w-72 sm:visible sm:w-full sm:h-16"
    :class="{ invisible: visible }"
  >
    <div
      class="flex flex-col m-auto items-center justify-between h-full w-full sm:flex-row"
    >
      <span class="grow"></span>
      <NavItem href="/#"> Dernières photos </NavItem>
      <NavItem href="/#team"> L'équipe </NavItem>
      <NavItem href="/" class="text-xl"> MiTV </NavItem>
      <NavItem href="/#hardware"> Le matériel </NavItem>
      <NavItem href="/#legal"> Mentions légales </NavItem>
      <span class="grow"></span>
      <NavItem href="/login" v-if="!$cookies.isKey('login')">
        <font-awesome-icon icon="fa-solid fa-user-gear" />
      </NavItem>
      <template v-else>
        <NavItem href="/upload">
          <font-awesome-icon icon="fa-solid fa-upload" />
        </NavItem>

        <NavItem href="#" @click="disconnect">
          <font-awesome-icon icon="fa-solid fa-right-from-bracket" />
        </NavItem>
      </template>
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
import http from "../http-common";

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
      this.visible = !this.visible;
    },
    disconnect() {
      http.post(
        "/disconnect",
        {
          login: this.$cookies.get("login"),
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      this.$cookies.remove("login");
      this.$forceUpdate();
    },
  },
});
</script>
