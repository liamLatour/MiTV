<!-- https://css-tricks.com/lazy-loading-images-with-vue-js-directives-and-intersection-observer/ -->

<template>
  <div
    class="viewer"
    v-bind:style="{ 'grid-template-columns': 'repeat(' + columns + ', 1fr)' }"
  >
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
      <span class="group" v-if="media.others != null">
        <font-awesome-icon icon="fa-solid fa-folder" />
      </span>
      <ImageItem
        v-if="media.type == 'pic'"
        :source="'http://127.0.0.1:5000/media_low_res/' + media.path"
        @click="openImage(index)"
        class="image"
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
  </div>

  <div
    class="modal"
    v-if="showModal"
    @click="showModal = false"
    v-bind:class="{ small: medias[currentImg].others == null }"
  >
    <div class="top">
      <div class="right-icons">
        <a :href="'http://127.0.0.1:5000/download/' + getModalImg()" download>
          <font-awesome-icon
            icon="fa-solid fa-download"
            class="download"
            v-on:click.stop
          />
        </a>
        <font-awesome-icon
          icon="fa-solid fa-times"
          class="close"
          @click="showModal = false"
        />
      </div>
    </div>
    <div class="modal-content">
      <div class="imgContainer">
        <img
          :src="'http://127.0.0.1:5000/media/' + getModalImg()"
          alt="image introuvable"
          v-on:click.stop
        />
      </div>
    </div>
    <div class="footer">
      <div class="others" v-if="medias[currentImg].others != null">
        <img
          v-for="path in medias[currentImg].others"
          :key="path"
          :src="'http://127.0.0.1:5000/media_low_res/' + path"
          alt="image introuvable"
          @click="changeModalImage(path)"
          v-on:click.stop
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ImageItem from "./ImageItem.vue";

export default defineComponent({
  name: "GalleryViewer",
  components: {
    ImageItem,
  },
  data: function () {
    return {
      showModal: false,
      currentImg: 0,
      modalImg: "",
      columns: 36,
    };
  },
  props: {
    medias: {
      type: Object,
      required: true,
    },
    isGlobal: {
      type: Boolean,
      default: false,
    },
  },
  created() {
    window.addEventListener("resize", this.windowSizeChange);
    this.windowSizeChange();
  },
  unmounted() {
    window.removeEventListener("resize", this.windowSizeChange);
  },
  methods: {
    openImage(i: string) {
      let index: number = parseInt(i);
      this.currentImg = index;
      this.showModal = true;
      this.modalImg = this.medias[index].path;
    },
    changeModalImage(path: string) {
      console.log(path);
      this.modalImg = path;
    },
    getModalImg() {
      return this.modalImg;
    },
    windowSizeChange() {
      console.log(window.innerWidth);
      let nb_columns = (window.innerWidth / 300) >> 0;
      this.columns = 9 * nb_columns;
    },
  },
});
</script>

<style scoped lang="scss">
.viewer {
  display: grid;
  //grid-template-columns: repeat(36, 1fr);

  .media {
    overflow: hidden;
    margin: 2px;
    grid-column: span 9;
    aspect-ratio: 3/2;

    .image {
      transition: transform 0.4s;
      cursor: pointer;

      &:hover {
        -ms-transform: scale(1.1); /* IE 9 */
        -webkit-transform: scale(1.1); /* Safari 3-8 */
        transform: scale(1.1);
      }
    }

    .group {
      position: absolute;
      bottom: 0;
      right: 0;
      z-index: 10;
      margin: 10px;
      font-size: 25px;
      color: rgba(255, 255, 255, 0.616);
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
    grid-column: span 4;
    aspect-ratio: 2/3;
  }
}

.modal {
  position: fixed; /* Stay in place */
  z-index: 100; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100vh; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.685); /* Black w/ opacity */

  .top {
    height: 50px;

    .right-icons {
      position: absolute;
      right: 10px;
      margin: 5px;
      color: rgb(255, 255, 255);
      font-size: 30px;

      a {
        all: unset;
      }

      svg {
        margin: 5px;
        margin-right: 15px;

        &:hover,
        &:focus {
          color: rgb(141, 141, 141);
          text-decoration: none;
          cursor: pointer;
        }
      }
    }
  }

  .modal-content {
    margin: auto;
    height: calc(100% - 50px - 150px);
    display: flex;

    .imgContainer {
      margin: auto;
      max-height: 100%;
      max-width: 100%;
      aspect-ratio: 3/2; //TODO: change that for portrait

      img {
        height: 100%;
        object-fit: cover;
      }
    }
  }

  .footer {
    height: 150px;
    .others {
      display: flex;
      justify-content: center;
      height: 140px;

      img {
        height: 100%;
        margin: 5px;
        cursor: pointer;
        transition: transform 0.1s;

        &:hover {
          -ms-transform: scale(1.05); /* IE 9 */
          -webkit-transform: scale(1.05); /* Safari 3-8 */
          transform: scale(1.05);
        }
      }
    }
  }
}

.small {
  .footer {
    height: 20px;
  }
  .modal-content {
    height: calc(100% - 50px - 20px);
  }
}
</style>
