<template>
    <section class="file-upload">
        <h1>{{ heading }}</h1>
        <img alt="Vue logo" class="file-icon" src="@/assets/file-picture-o.svg">
        <div class="custom-file-upload">
            <div class="file-upload-wrapper">
                <input type="file"
                       id="files"
                       class="custom-file-upload-hidden"
                       ref="files"
                       multiple
                       accept="image/png"
                       @change="handleUploadFiles()"/>
                <input type="text" class="file-upload-input" :title="fileNames" v-model="fileNames">
                <button class="select-files-button button" @click="triggerChangeOnFilesInput">SELECT FILES</button>
            </div>
            <button class="file-upload-button button" @click="submitFiles">SUBMIT FILES</button>
        </div>
    </section>
</template>

<script>
export default {
    name: "FileUpload",
    data() {
        return {
            files: [],
            heading: 'Upload your files!'
        }
    },
    computed: {
        filesSelected() {
            return this.files.length > 0
        },
        fileNames() {
            return this.filesSelected ? Array.from(this.files).map(file => file.name).join('; ') : ''
        }
    },
    methods: {
        triggerChangeOnFilesInput() {
            this.$refs.files.click()
        },
        handleUploadFiles() {
            this.files = this.$refs.files.files;
        },
        submitFiles() {
            let formData = new FormData();
            this.files.forEach((file, i) => formData.append('files[' + i + ']', file));
            this.$http.post( 'http://localhost:5000/upload-files',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(response => {
                console.log(`SUCCESS!! Response: ${response.data}`);
                this.resetFiles();
                this.heading = 'Thank you for your files!'
            }).catch(error => {
                console.error(`FAILURE!! ${error}`);
                this.resetFiles();
                this.heading = 'Something went wrong...'
            });
        },
        resetFiles() {
            this.files = []
        }
    }
}
</script>

<style scoped>

</style>