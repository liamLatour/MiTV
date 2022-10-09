<template>
  <div class="gear">
    <h2>{{ name }}</h2>
    <h3>{{ type }}</h3>
    <h4>{{ reference }}</h4>
  </div>
</template>

<script lang="ts">
export default {
  name: "PhotoGear",
  props: {
    type: {
      type: String,
    },
    name: {
      type: String,
    },
    reference: {
      type: String,
    },
  },
};
</script>

<style scoped lang="scss">
.gear {
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

  h4 {
    margin-top: 10px;
    color: rgba(255, 255, 255, 0.521);
  }
}
</style>
