<template>
    <section class="image-upload">
        <h1>{{ heading }}</h1>
        <img alt="Vue logo" class="image-icon" src="@/assets/file-picture-o.svg">
        <div class="custom-file-upload">
            <div class="file-upload-wrapper">
                <input type="file"
                       id="images"
                       class="custom-file-upload-hidden"
                       ref="images"
                       multiple
                       accept="image/png"
                       @change="handleUploadImages()"/>
                <input type="text" class="file-upload-input" :title="imageNames" v-model="imageNames">
                <button class="select-images-button button" @click="triggerChangeOnImagesInput">SELECT IMAGES</button>
            </div>
            <button class="file-upload-button button" @click="submitImages">SUBMIT IMAGES</button>
        </div>
    </section>
</template>

<script>
export default {
    name: "ImageUpload",
    data() {
        return {
            images: [],
            heading: 'Upload your images!'
        }
    },
    computed: {
        imagesSelected() {
            return this.images.length > 0
        },
        imageNames() {
            return this.imagesSelected ? Array.from(this.images).map(image => image.name).join('; ') : ''
        }
    },
    methods: {
        triggerChangeOnImagesInput() {
            this.$refs.images.click()
        },
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
                this.resetImages();
                this.heading = 'Thank you for your images!'
            }).catch(error => {
                console.error(`FAILURE!! ${error}`);
                this.resetImages();
                this.heading = 'Something went wrong...'
            });
        },
        resetImages() {
            this.images = []
        }
    }
}
</script>

<style scoped>

</style>