<template>
  <div class="member">
    <h2>{{ role }}</h2>
    <h3>{{ prenom }}</h3>
    <h3>{{ nom }}</h3>
  </div>
</template>

<script lang="ts">
export default {
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
};
</script>

<style scoped lang="scss">
.member {
  background-color: rgb(39, 38, 31);
  text-align: center;
  padding: 20px;
  margin: 20px;
  border-radius: 5px;
  width: 250px;

  h2 {
    font-weight: 600;
    margin-bottom: 10px;
  }
}
</style>
