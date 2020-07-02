<template>
  <div id="app">

    <ImageUpload></ImageUpload>
  </div>
</template>

<script>
import ImageUpload from "./components/ImageUpload";

export default {
  name: 'App',
  components: {
    ImageUpload
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
.image-icon {
  max-width: 8em;
  margin-top: 2em;
}
</style>
