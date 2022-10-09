<template>
  <div class="landing fullpage">
    <img src="../assets/paysage.jpg" alt="" />
    <div class="tagline">
      <h2>Rendre vos années mémorables</h2>
      <a href="/photos/photos">Voir les photos</a>
    </div>
  </div>
  <div class="team fullpage">
    <h2>L'équipe</h2>
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
  <div class="hardware fullpage"></div>
  <div class="legal fullpage">
    <!--https://entreprendre.service-public.fr/vosdroits/F31228/personnalisation/resultat?lang=&quest0=0&quest=-->
    <h1>C'est pas de nôtre faute</h1>
    <p>Je te promet si tu fais de la merde je te casse la gueule</p>
  </div>
</template>

<script lang="ts">
import Member from "../components/Member.vue";

export default {
  name: "HomeView",
  components: {
    Member: Member,
  },
};
</script>

<style scoped lang="scss">
.fullpage {
  height: 100vh;
  overflow: clip;
}

.team {
  background-color: rgb(34, 26, 26);
  h2 {
    font-size: 3em;
    font-weight: 700;
    margin: auto;
    text-align: center;
    padding: 20px;
    margin-bottom: 50px;
  }

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

.hardware {
  background-color: rgb(25, 25, 32);
}

.landing {
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
