<template>
  <div class="text-center rounded bg-neutral-900 m-1 p-3 sm:w-52 sm:p-5 sm:m-5">
    <h2 class="font-semibold mb-2">{{ role }}</h2>
    <h3 class="">{{ prenom }}</h3>
    <h3 class="">{{ nom }}</h3>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  name: "MemberDisplay",
  props: {
    role: {
      type: String,
    },
    nom: {
      type: String,
    },
    prenom: {
      type: String,
    },
  },
});
</script>
