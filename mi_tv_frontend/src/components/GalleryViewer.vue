<template>
  <div class="viewer">
    <!--
    <div class="media portrait" v-if="isglobal">
      <div>
        <img
          src="http://127.0.0.1:5000/media_low_res/people_ref/liam.jpg"
          alt="image introuvable"
        />
        <a href="/mes_photos" class="overlay">
          <h2 class="dirname">Mes Photos</h2>
        </a>
      </div>
    </div>-->
    <div
      class="media"
      v-for="(media, index) in medias"
      :key="media.path"
      v-bind:class="{ portrait: media.is_portrait }"
    >
      <img
        v-if="media.type == 'pic'"
        :src="'http://127.0.0.1:5000/media_low_res/' + media.path"
        alt="image introuvable"
        @click="openImage(index)"
      />
      <div v-if="media.type == 'dir'">
        <img
          :src="'http://127.0.0.1:5000/media_low_res/' + media.thumbnail"
          alt="image introuvable"
        />
        <a :href="media.path" class="overlay">
          <h2 class="dirname">
            {{ media.event_name }}
          </h2>
        </a>
      </div>
    </div>
    <div class="media" v-for="n in 10" :key="n"></div>
  </div>

  <div class="modal" v-if="showModal" @click="showModal = false">
    <span class="close" @click="showModal = false">&times;</span>
    <div class="modal-content">
      <div class="imgContainer">
        <img
          :src="'http://127.0.0.1:5000/media/' + medias[currentImg].path"
          alt="image introuvable"
          v-on:click.stop
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "GalleryViewer",
  data: function () {
    return {
      showModal: false,
      currentImg: 0,
    };
  },
  props: {
    medias: {
      type: Object,
    },
    isglobal: {
      type: Boolean,
    },
  },
  methods: {
    openImage(i: number) {
      this.currentImg = i;
      this.showModal = true;
    },
  },
};
</script>

<style scoped lang="scss">
.viewer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  align-items: flex-start;

  .media {
    flex-shrink: 1;
    flex-grow: 1;
    width: 300px;
    //height: 200px;
    overflow: hidden;
    margin: 2px;

    img {
      transition: transform 0.1s;
      width: 100%;
      height: 100%;

      &:hover {
        -ms-transform: scale(1.05); /* IE 9 */
        -webkit-transform: scale(1.05); /* Safari 3-8 */
        transform: scale(1.05);
        cursor: pointer;
      }
    }
    .overlay {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      top: 0;
      background-color: rgba(0, 0, 0, 0.5);

      .dirname {
        position: absolute;
        left: 0;
        right: 0;
        top: calc(50% - 24px);
        text-align: center;
        font-size: 30px;
      }
    }
  }

  .portrait {
    width: 133px;
    //height: 200px;
  }
}

.modal {
  position: fixed; /* Stay in place */
  z-index: 100; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.685); /* Black w/ opacity */

  .modal-content {
    margin: 50px auto 20px auto;
    height: calc(100% - 70px);

    .imgContainer {
      margin: auto;
      max-height: 100%;
      aspect-ratio: 3/2;

      img {
        position: absolute;
        top: 0;
        height: 100%;
      }
    }
  }

  .close {
    color: rgb(255, 255, 255);
    float: right;
    font-size: 40px;
    font-weight: bold;
    margin-right: 30px;
    line-height: 50px;

    &:hover,
    &:focus {
      color: rgb(141, 141, 141);
      text-decoration: none;
      cursor: pointer;
    }
  }
}
</style>
