<template>
  <div
    class="fixed z-30 left-0 top-0 bottom-0 right-0 flex flex-col bg-black bg-opacity-70"
    v-if="show"
    @click="$emit('close')"
    :class="{ small: images.length == 1 }"
  >
    <!--Header-->
    <div class="h-12">
      <div class="absolute right-2 m-1 text-white text-3xl">
        <a
          :href="backendURL + 'download/' + images[currentImg]"
          class=""
          download
        >
          <font-awesome-icon
            icon="fa-solid fa-download"
            class="m-1 mr-4 hover:text-gray-300"
            v-on:click.stop
          />
        </a>
        <font-awesome-icon
          icon="fa-solid fa-times"
          class="m-1 mr-4 hover:text-gray-300 cursor-pointer"
          @click="$emit('close')"
        />
      </div>
    </div>

    <!--Image-->
    <div class="m-auto min-h-0 min-w-0">
      <img
        :src="backendURL + 'media/' + images[currentImg]"
        alt="image introuvable"
        v-on:click.stop
        ref="image"
        @loadstart="buffering = true"
        class="max-h-full max-w-full m-auto"
        id="img1"
      />
      <div class="absolute inset-0 flex justify-center items-center z-50">
        <font-awesome-icon
          icon="fa-solid fa-spinner"
          class="animate-spin text-8xl"
          v-if="buffering"
        />
      </div>
    </div>

    <!--Footer-->
    <div class="text-center">
      <span>{{ currentDate }}</span>
      <div class="flex justify-center h-36" v-if="images.length > 1">
        <img
          v-for="(url, index) in images"
          :key="index"
          :src="backendURL + 'media_low_res/' + url"
          class="h-full p-1 cursor-pointer image-anim"
          alt="image introuvable"
          @click="currentImg = index"
          v-on:click.stop
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { backendURL } from "../http-common";

export default defineComponent({
  name: "ImageModal",
  props: {
    images: {
      type: Array,
      required: true,
    },
    show: {
      type: Boolean,
      default: false,
    },
    timestamp: {
      type: Number,
    },
    backendURL: {
      type: String,
      default: backendURL,
    },
  },
  data: function () {
    return {
      currentImg: 0,
      buffering: true,
    };
  },
  computed: {
    currentDate: function () {
      console.log(this.timestamp);
      let d = new Date(this.timestamp * 1000);

      let dformat =
        [d.getFullYear(), d.getMonth() + 1, d.getDate()].join("/") +
        " " +
        " " +
        [d.getHours(), d.getMinutes(), d.getSeconds()].join(":");
      return dformat;
    },
  },
});
</script>
