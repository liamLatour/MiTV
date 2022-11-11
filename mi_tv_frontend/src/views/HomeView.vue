<template>
  <div id="landing" class="h-screen overflow-clip">
    <img
      src="../assets/paysage.jpg"
      alt=""
      class="min-h-screen min-w-full max-w-none grayscale blur-sm"
    />
    <div class="absolute maxed right-24 top-24 aspect-square">
      <div class="absolute h-3/4 w-full bottom-0">
        <img
          src="../assets/illustration_1.jpg"
          alt=""
          class="absolute w-2/3 top-0 left-0"
        />
        <img
          src="../assets/illustration_3.jpg"
          alt=""
          class="absolute w-2/3 bottom-0 right-0"
        />
      </div>
      <img
        src="../assets/illustration_2.jpg"
        alt=""
        class="absolute w-2/5 top-0 right-sm"
      />
    </div>
    <div
      class="absolute left-8 bottom-20 text-2xl w-72 leading-snug sm:w-max sm:max-w-sm sm:leading-snug sm:text-5xl sm:left-20 sm:bottom-20"
    >
      <h2>Rendre vos années mémorables</h2>
      <router-link
        to="/photos/photos"
        class="text-cyan-400 hover:text-cyan-200"
      >
        Voir les photos
      </router-link>
    </div>
    <div class="tilt">
      <svg
        data-name="Layer 1"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 1200 120"
        preserveAspectRatio="none"
      >
        <path
          d="M1200 120L0 16.48 0 0 1200 0 1200 120z"
          class="shape-fill"
        ></path>
      </svg>
    </div>
  </div>
  <div class="h-screen overflow-clip indigo">
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

<style scoped>
.maxed {
  width: 100%;
  max-width: 60%;
  aspect-ratio: 1 / 1;
}

.right-sm {
  right: 10%;
}

.tilt {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
  transform: rotate(180deg);
}

.tilt svg {
  position: relative;
  display: block;
  width: calc(100% + 1.3px);
  height: 56px;
}

.tilt .shape-fill {
  fill: hsl(242, 15%, 10%);
}

.indigo {
  background-color: hsl(242, 15%, 10%);
}

/** For tablet devices **/
@media (min-width: 768px) and (max-width: 1023px) {
  .tilt svg {
    width: calc(100% + 1.3px);
    height: 60px;
  }
}
</style>
