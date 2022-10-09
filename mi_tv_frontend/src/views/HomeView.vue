<template>
  <div id="landing" class="fullpage">
    <img src="../assets/paysage.jpg" alt="" />
    <div class="tagline">
      <h2>Rendre vos années mémorables</h2>
      <a href="/photos/photos">Voir les photos</a>
    </div>
  </div>
  <div id="team" class="fullpage">
    <h2 class="title">L'équipe</h2>
    <div class="members">
      <Member role="Trésorier" nom="PHALIPPOU--GELABERT" prenom="Donatien" />
      <Member role="Président" nom="CHAZALON" prenom="Louis" />
      <Member role="Secrétaire" nom="GUERRIERI" prenom="Hugo" />
    </div>
    <hr />
    <div class="members">
      <Member role="Membre" nom="POTTIER" prenom="Etienne" />
      <Member role="Membre" nom="ANDRE" prenom="Victor" />
      <Member role="Membre" nom="PORTIER" prenom="Aurélien" />
      <Member role="Membre" nom="VILLENEUVE" prenom="Paul" />
      <Member role="Membre" nom="CHENG" prenom="Ruining" />
      <Member role="Membre" nom="TAUPEAU" prenom="Eva" />
      <Member role="Membre" nom="GUERIN" prenom="Gabriel" />
    </div>
  </div>
  <div id="hardware" class="fullpage">
    <h2 class="title">Le matériel</h2>
    <div class="gearlist">
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
  <div id="legal" class="fullpage">
    <h2 class="title">Mention légales</h2>

    <!--https://entreprendre.service-public.fr/vosdroits/F31228/personnalisation/resultat?lang=&quest0=0&quest=-->
    <h1>C'est pas de nôtre faute</h1>
    <p>Je te promet si tu fais de la merde je te casse la gueule</p>
  </div>
</template>

<script lang="ts">
import Member from "../components/Member.vue";
import PhotoGear from "../components/PhotoGear.vue";

export default {
  name: "HomeView",
  components: {
    Member: Member,
    PhotoGear: PhotoGear,
  },
};
</script>

<style scoped lang="scss">
.fullpage {
  height: 100vh;
  overflow: clip;
}

.title {
  font-size: 3em;
  font-weight: 700;
  margin: auto;
  text-align: center;
  padding: 20px;
  margin-bottom: 50px;
}

#team {
  background-color: rgb(34, 26, 26);

  hr {
    width: 60%;
    margin: auto;
    margin-bottom: 20px;
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.137);
  }

  .members {
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;

    width: 70%;
    margin: auto;
  }
}

#hardware {
  background-color: rgb(25, 25, 32);

  .gearlist {
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;

    width: 70%;
    margin: auto;
  }
}

#landing {
  img {
    min-width: 100%;
    min-height: 100%;
  }
  .tagline {
    position: absolute;
    bottom: 0;
    margin: 100px;
    font-size: 40px;
    width: 400px;
    line-height: 70px;

    h2 {
      margin-bottom: 60px;
    }
  }
}
</style>
