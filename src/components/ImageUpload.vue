<template>
    <div class="container">
        <label>File
            <input type="file" id="images" ref="images" multiple accept="image/png" @change="handleUploadImages()"/>
        </label>
        <button @click="submitImages()">Submit</button>
    </div>
</template>

<script>
export default {
    name: "ImageUpload",
    data() {
        return {
            images: []
        }
    },
    methods: {
        handleUploadImages() {
            this.images = this.$refs.images.files;
        },
        submitImages() {
            let formData = new FormData();
            this.images.forEach((image, i) => formData.append('images[' + i + ']', image));
            this.$http.post( 'http://localhost:5000/upload-images',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(response => {
                console.log(`SUCCESS!! Response: ${response.data}`);
            }).catch(error => {
                console.error(`FAILURE!! ${error}`);
            });
        }
    }
}
</script>

<style scoped>

</style>