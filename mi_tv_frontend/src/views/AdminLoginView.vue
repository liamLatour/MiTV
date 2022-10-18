<!--https://www.bezkoder.com/vue-upload-image-axios/ -->

<template>
  <h1 class="text-center mt-10 text-3xl mb-20 sm:text-6xl sm:mt-16">Login</h1>

  <form
    class="w-11/12 flex flex-col items-stretch justify-center max-w-lg m-auto"
    @submit="login"
  >
    <label class="m-2 text-lg" for="username">Nom d'utilisateur</label>
    <input
      class="align-middle p-1 border bg-transparent md:m-3"
      type="text"
      id="username"
      v-model="username"
      name="username"
    />
    <label class="m-2 text-lg" for="password">Mot de passe</label>
    <input
      class="align-middle p-1 border bg-transparent md:m-3"
      type="password"
      id="password"
      v-model="password"
      name="password"
    />
    <input
      class="text-lg p-1 w-20 m-auto bg-teal-600 rounded mt-4 cursor-pointer hover:bg-teal-500"
      type="submit"
      value="Envoyer"
    />
  </form>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import http from "../http-common";

export default defineComponent({
  name: "UploadView",
  components: {},
  data() {
    return {
      password: "",
      username: "",
    };
  },
  methods: {
    login(e: Event) {
      e.preventDefault();
      http
        .post(
          "/login",
          {
            username: this.username,
            password: this.password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((response) => {
          let res = response.data["res"];
          if (res != false) {
            this.$cookies.set("login", res);
            this.$router.go(-1);
          } else {
            alert("Mauvais identifiants");
          }
        });
    },
  },
});
</script>
