<template>
  <div
    class="fixed z-30 left-0 top-0 bottom-0 right-0 flex flex-col bg-black bg-opacity-70"
    v-if="show"
  >
    <!--Header-->
    <div class="h-12" ref="header">
      <div class="absolute right-2 m-1 text-white text-3xl">
        <a :href="backendURL + 'vdownload/' + video" class="" download>
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

    <!--Video-->
    <div class="m-auto min-h-0 min-w-0 z-40">
      <div>
        <video
          ref="video"
          :src="backendURL + 'vmedia/' + video"
          autoplay="true"
          loop="true"
          disablePictureInPicture
          v-bind:style="[
            phone ? { width: vidDim + 'px' } : { height: vidDim + 'px' },
          ]"
          @timeupdate="updateTime"
          @waiting="buffering = true"
          @canplay="buffering = false"
        ></video>

        <div
          class="absolute inset-0 flex justify-center items-center z-50"
          @click="togglePlay"
          @mouseenter="fadeManager(false)"
          @mouseleave="fadeManager(true)"
        >
          <font-awesome-icon
            v-if="buffering"
            icon="fa-solid fa-spinner"
            class="text-8xl image-anim"
          />
          <font-awesome-icon
            v-if="playing && opacity > 0.05 && !buffering"
            v-bind:style="{ opacity: opacity }"
            icon="fa-solid fa-pause"
            class="text-8xl"
          />
          <font-awesome-icon
            v-if="paused && !buffering"
            v-bind:style="{ opacity: opacity }"
            icon="fa-solid fa-play"
            class="text-8xl"
          />
        </div>
      </div>

      <div class="inset-0 flex flex-nowrap flex-row justify-center">
        <div class="flex-none my-auto">
          <div>
            <span>{{ elapsedTime }}</span> /
            <span>{{ totalTime }}</span>
          </div>
        </div>

        <div
          class="grow m-2 rounded-lg progress-container"
          ref="totalBar"
          @click="setTime"
        >
          <div
            class="rounded-lg progress h-full"
            ref="progressBar"
            v-bind:style="{ width: progressWidth + 'px' }"
          ></div>
        </div>

        <div class="flex-none my-auto">
          <div class="flex flex-nowrap flex-row">
            <font-awesome-icon
              icon="fa-solid fa-volume-low"
              class="text-3xl ml-4"
            />
            <div
              class="grow m-2 rounded-lg progress-container w-20"
              ref="totalVolume"
              @click="setVolume"
            >
              <div
                class="rounded-lg progress h-full"
                ref="volumeBar"
                v-bind:style="{ width: volumeWidth + 'px' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { backendURL } from "../http-common";

export default defineComponent({
  name: "VideoModal",
  props: {
    video: {
      type: String,
      required: true,
    },
    show: {
      type: Boolean,
      default: false,
    },
    backendURL: {
      type: String,
      default: backendURL,
    },
  },
  data() {
    return {
      opacity: 0.8,
      paused: false,
      buffering: false,
      timer: -1,
      elapsedTime: "",
      totalTime: "",
      progressWidth: 0,
      volumeWidth: 0,
      vidDim: 360,
      phone: false,
    };
  },
  methods: {
    updateTime(event: Event) {
      if (this.$refs.video === null) {
        return;
      }

      let current = (this.$refs.video as HTMLVideoElement).currentTime;
      this.elapsedTime = this.formatTime(current);

      let duration = -1;

      if (!Number.isNaN((this.$refs.video as HTMLVideoElement).duration)) {
        duration = (this.$refs.video as HTMLVideoElement).duration;
      }

      if (duration > 0) {
        this.totalTime = this.formatTime(duration);
      } else {
        this.totalTime = "Temps inconnu";
      }

      if (duration > 0) {
        this.progressWidth = Math.floor(
          ((this.$refs.totalBar as HTMLElement).clientWidth * current) /
            duration
        );
      } else {
        this.progressWidth = Math.floor(
          (this.$refs.totalBar as HTMLElement).clientWidth / 2
        );
      }
    },
    formatTime(num: number) {
      let hours = Math.floor(num / 3600);
      let minutes = Math.floor((num % 3600) / 60);
      let seconds = Math.floor(num % 60);

      let str = "";

      if (hours > 0) {
        str += String(hours < 10 ? "0" + hours : hours);
        str += ":";
      }

      str += String(minutes < 10 ? "0" + minutes : minutes);
      str += ":";
      str += String(seconds < 10 ? "0" + seconds : seconds);

      return str;
    },
    togglePlay() {
      this.opacity = 0.8;

      if ((this.$refs?.video as HTMLVideoElement).paused) {
        (this.$refs?.video as HTMLVideoElement).play();
        this.paused = false;
      } else {
        (this.$refs?.video as HTMLVideoElement).pause();
        this.paused = true;
      }
    },
    fadeManager(out: boolean) {
      if (this.timer >= 0) {
        clearInterval(this.timer);
        this.timer = -1;
      }

      this.fade(out);
    },
    fade(out: Boolean) {
      if (this.paused) {
        return;
      }

      let that = this;

      this.timer = setInterval(function () {
        if (out) {
          that.opacity *= 0.8;

          if (that.opacity < 0.05) {
            clearInterval(that.timer);
            that.timer = -1;
          }
        } else {
          that.opacity *= 1.5;

          if (that.opacity > 0.8) {
            clearInterval(that.timer);
            that.timer = -1;
          }
        }
      }, 50);
    },
    setTime(event: MouseEvent) {
      const newTime =
        ((this.$refs.video as HTMLVideoElement).duration * event.offsetX) /
        (this.$refs.totalBar as HTMLElement).clientWidth;
      (this.$refs.video as HTMLVideoElement).currentTime = newTime;
    },
    setVolume(event: MouseEvent) {
      const volume =
        event.offsetX / (this.$refs.totalVolume as HTMLElement).clientWidth;
      (this.$refs.video as HTMLVideoElement).volume = volume;

      this.volumeWidth = event.offsetX;
    },
    setVolumeVal(val: number) {
      (this.$refs.video as HTMLVideoElement).volume = val;

      this.volumeWidth = Math.round(
        (this.$refs.totalVolume as HTMLElement).clientWidth * val
      );
    },
    onResize() {
      if (this.$refs.video == undefined || this.$refs.video == null || (this.$refs.video as HTMLVideoElement).readyState < 1) {
          return;
      }
      
      const ratio =
        ((this.$refs.video as HTMLVideoElement).videoWidth /
          (this.$refs.video as HTMLVideoElement).videoHeight) *
        0.9;

      if (window.innerWidth / window.innerHeight < ratio) {
        this.phone = true;
        this.vidDim = window.innerWidth;
      } else {
        this.phone = false;
        this.vidDim = Math.round(
          (window.innerHeight -
            (this.$refs.header as HTMLElement).clientHeight) *
            0.75
        );
      }
    },
    init() {
      if (this.$refs.video != null) {
        if ((this.$refs.video as HTMLVideoElement).readyState > 0) {
          this.onResize();
          this.setVolumeVal(0.8);
          (this.$refs.video as HTMLVideoElement).disablePictureInPicture = true;
          return;
        }
      }

      setTimeout(this.init, 50);
    },
  },
  computed: {
    playing() {
      return !this.paused;
    },
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
      this.init();
    });
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.onResize);
  },
});
</script>

<style lang="scss">
.progress-container {
  background: rgba(224, 224, 224, 0.5);
}

.progress {
  background: rgb(224, 224, 224);
}

.image-anim {
  transition: transform 0.4s;

  &:hover {
    -ms-transform: scale(1.1); /* IE 9 */
    -webkit-transform: scale(1.1); /* Safari 3-8 */
    transform: scale(1.1);
  }
}
</style>
