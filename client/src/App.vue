<template>
  <div id="app">

    <FileUpload></FileUpload>
  </div>
</template>

<script>
import FileUpload from "./components/FileUpload";

export default {
  name: 'App',
  components: {
    FileUpload
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
