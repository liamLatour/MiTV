<template>
  <div id="landing" class="h-screen overflow-clip">
    <img
      src="../assets/paysage.jpg"
      alt=""
      class="min-h-screen min-w-full max-w-none"
    />
    <div
      class="absolute left-8 bottom-8 sm:left-20 sm:bottom-20 text-2xl w-72 leading-snug sm:w-96 sm:leading-snug sm:text-4xl"
    >
      <h2>Rendre vos années mémorables</h2>
      <h3><router-link to="/photos/photos">Voir les photos</router-link></h3>
    </div>
  </div>
  <div id="team" class="h-screen overflow-clip bg-indigo-900 bg-opacity-10">
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

    <!--https://entreprendre.service-public.fr/vosdroits/F31228/personnalisation/resultat?lang=&quest0=0&quest=-->
    <h2>C'est pas de nôtre faute</h2>
    <p>Je te promet si tu fais de la merde je te casse la gueule</p>
  </div>
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
