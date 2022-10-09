<template>
  <div class="navbar">
    <div class="navbar-content">
      <a href="#">Dernières photos</a>
      <a href="#">L'équipe</a>
      <a href="/" class="title">MiTV</a>
      <a href="#">Le matériel</a>
      <a href="#">Mentions légales</a>
    </div>
  </div>

  <RouterView />
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<style lang="scss">
.navbar {
  position: absolute;
  width: 100%;
  height: 65px;
  background-color: rgb(39, 36, 36);
  z-index: 10;

  .navbar-content {
    max-width: 1070px;
    height: inherit;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;

    a {
      padding: 5px;
      font-weight: 700;

      &.title {
        font-size: 20px;
      }
    }
  }
}
</style>
