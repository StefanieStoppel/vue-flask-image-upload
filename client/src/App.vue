<template>
  <div id="app">

    <FileUpload @pointCloudUrlsReceived="onPointCloudUrlsFetched"/>

    <div class="pcd-container" id="pcd-container">
      <PCDViewer v-for="pointCloudUrl in pointCloudUrls" :key="pointCloudUrl" :pointCloudUrl="pointCloudUrl"/>
    </div>
  </div>
</template>

<script>
import FileUpload from "./components/FileUpload";
import PCDViewer from "./components/PCDViewer";

export default {
  name: 'App',
  components: {
    FileUpload,
    PCDViewer
  },
  data() {
    return {
      pointCloudUrls: []
    }
  },
  methods: {
    onPointCloudUrlsFetched(urls) {
      this.pointCloudUrls = urls
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #f54291;
  margin-top: 60px;
}
.file-icon {
  max-width: 8em;
  margin-top: 2em;
}
.pcd-container {
  margin-top: 3em;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-auto-rows: 1fr;
  grid-gap: 2em;
}
</style>
