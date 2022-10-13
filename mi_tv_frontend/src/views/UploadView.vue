<!--https://www.bezkoder.com/vue-upload-image-axios/-->

<template>
  <h1 class="title">Uploadez vos images</h1>
  <form action="" method="get" class="form-example">
    <div class="form-example">
      <label for="name">Enter your name: </label>
      <input type="text" name="name" id="name" required />
    </div>
    <div class="form-example">
      <label for="email">Enter your email: </label>
      <input type="email" name="email" id="email" required />
    </div>
    <div class="form-example">
      <input type="submit" value="Subscribe!" />
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "UploadView",
});
</script>

<style lang="scss" scoped>
.title {
  text-align: center;
  padding-top: 70px;
}
</style>
