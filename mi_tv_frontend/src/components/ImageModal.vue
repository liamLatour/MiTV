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
          :href="'http://backend:5000/download/' + images[currentImg]"
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
        :src="'http://backend:5000/media/' + images[currentImg]"
        alt="image introuvable"
        v-on:click.stop
        ref="image"
        @loadstart="buffering = true"
        @load="getEXIF(); buffering = false"
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
          :src="'http://backend:5000/media_low_res/' + url"
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
import EXIF from "exif-js";

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
  },
  data: function () {
    return {
      currentImg: 0,
      currentDate: "",
      buffering: true,
    };
  },
  methods: {
    getEXIF() {
      let image = this.$refs.image as HTMLImageElement;
      let url = this.$refs.image as string; // Only to please typescript
      let that = this;

      EXIF.getData(url, function () {
        console.log(EXIF.getAllTags(image));

        const date = that.parseDate(EXIF.getTag(image, "DateTime"));
        that.currentDate = date.toLocaleString();
      });
    },
    parseDate(date: string) {
      let parts = date.match(/(\d+)/g);

      return new Date(
        parseInt(parts![0]),
        parseInt(parts![1]) - 1,
        parseInt(parts![2]),
        parseInt(parts![3]),
        parseInt(parts![4])
      );
    },
  },
});
</script>
