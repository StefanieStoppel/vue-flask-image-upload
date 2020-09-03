<template>
  <div id="app">

    <FileUpload @pointCloudUrlsReceived="onPointCloudUrlsFetched"/>

    <PCDViewer v-for="pointCloudUrl in pointCloudUrls" :key="pointCloudUrl" :pointCloudUrl="pointCloudUrl"/>
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
</style>
