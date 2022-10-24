<template>
  <div id="landing" class="h-screen overflow-clip">
    <img
      src="../assets/paysage.jpg"
      alt=""
      class="min-h-screen min-w-full max-w-none grayscale blur-sm"
    />
    <div class="absolute w-1/2 h-2/4 left-1/3 bottom-1/4">
      <img
        src="../assets/illustration_1.jpg"
        alt=""
        class="absolute w-full mr-32"
      />
    </div>
    <div
      class="absolute left-8 bottom-8 text-2xl w-72 leading-snug sm:w-max sm:max-w-sm sm:leading-snug sm:text-5xl sm:left-20 sm:bottom-20"
    >
      <h2>Rendre vos années mémorables</h2>
      <router-link
        to="/photos/photos"
        class="text-cyan-400 hover:text-cyan-200"
      >
        Voir les photos
      </router-link>
    </div>
  </div>
  <div class="h-screen overflow-clip bg-indigo-900 bg-opacity-10">
    <span id="team" class="absolute -top-11"></span>
    <h1 class="text-center text-3xl p-4 sm:text-6xl">L'équipe</h1>
    <div class="flex items-center justify-around flex-wrap max-w-4xl m-auto">
      <Member role="Trésorier" nom="PHALIPPOU--GELABERT" prenom="Donatien" />
      <Member role="Président" nom="CHAZALON" prenom="Louis" />
      <Member role="Secrétaire" nom="GUERRIERI" prenom="Hugo" />
    </div>
    <hr class="w-2/3 m-auto border-gray-600" />
    <div class="flex items-center justify-around flex-wrap max-w-4xl m-auto">
      <Member role="Membre" nom="POTTIER" prenom="Etienne" />
      <Member role="Membre" nom="ANDRE" prenom="Victor" />
      <Member role="Membre" nom="PORTIER" prenom="Aurélien" />
      <Member role="Membre" nom="VILLENEUVE" prenom="Paul" />
      <Member role="Membre" nom="CHENG" prenom="Ruining" />
      <Member role="Membre" nom="TAUPEAU" prenom="Eva" />
      <Member role="Membre" nom="GUERIN" prenom="Gabriel" />
    </div>
  </div>
  <!--
  <div id="hardware" class="h-screen overflow-clip bg-red-900 bg-opacity-10">
    <h1 class="text-center text-3xl p-4 sm:text-6xl">Le matériel</h1>
    <div class="flex items-center justify-around flex-wrap max-w-4xl m-auto">
      <PhotoGear
        type="Appareil photo"
        name="Nikon d3500"
        reference="Reflex Nikon D3500 Noir"
      />
      <PhotoGear type="Membre" name="GUERIN" reference="Gabriel" />
      <PhotoGear type="Membre" name="GUERIN" reference="Gabriel" />
      <PhotoGear type="Membre" name="GUERIN" reference="Gabriel" />
    </div>
  </div>
  <div id="legal" class="h-screen overflow-clip bg-teal-900 bg-opacity-10">
    <h1 class="text-center text-3xl p-4 sm:text-6xl">Mention légales</h1>

  </div>
  -->
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Member from "../components/Member.vue";
import PhotoGear from "../components/PhotoGear.vue";

export default defineComponent({
  name: "HomeView",
  components: {
    Member: Member,
    PhotoGear: PhotoGear,
  },
});
</script>
