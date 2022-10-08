<template>
  <div class="viewer">
    <div class="media" v-if="isglobal">
      <div>
        <img
          src="http://127.0.0.1:5000/media/people_ref/liam.jpg"
          alt="image introuvable"
        />
        <a href="/mes_photos" class="overlay">
          <h2 class="dirname">Mes Photos</h2>
        </a>
      </div>
    </div>
    <div class="media" v-for="media in medias" :key="media.path">
      <img
        v-if="media.type == 'pic'"
        :src="'http://127.0.0.1:5000/media/' + media.path"
        alt="image introuvable"
      />
      <div v-if="media.type == 'dir'">
        <img
          :src="'http://127.0.0.1:5000/media/' + media.thumbnail"
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
</template>

<script lang="ts">
export default {
  name: "GalleryViewer",
  props: {
    medias: {
      type: Object,
    },
    isglobal: {
      type: Boolean,
    },
  },
};
</script>

<style scoped lang="scss">
.viewer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;

  .media {
    flex-shrink: 1;
    flex-grow: 1;
    width: 300px;
    overflow: hidden;

    img {
      transition: transform 0.1s;
      width: 100%;
      height: 100%;

      &:hover {
        -ms-transform: scale(1.05); /* IE 9 */
        -webkit-transform: scale(1.05); /* Safari 3-8 */
        transform: scale(1.05);
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
}
</style>
