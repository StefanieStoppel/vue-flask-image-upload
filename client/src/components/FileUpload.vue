<template>
    <section class="file-upload">
        <h1>{{ heading }}</h1>
        <img alt="Picture icon" class="file-icon" src="@/assets/file-picture-o.svg">
        <div class="custom-file-upload">
            <div class="select">
                <label class="select-label" for="ycb-object-class">
                    YCB OBJECT CLASS
                </label>
                <select id="ycb-object-class" class="select-hidden">
                    <option value="hide">-- YCB OBJECT CLASS --</option>
                    <option v-for="objectClass in objectClasses"
                            :key="objectClass.displayName"
                            :ref="`object-${objectClass.displayName}`"
                            :value="objectClass.value">
                        {{ objectClass.displayName }}
                    </option>
                </select>
                <div class="select-styled active"
                     ref="class-select"
                     @click="toggleShowSelectDropdown">
                    {{ chosenObjectClass.displayName || chosenObjectClass }}
                </div>
                <ul class="select-options" :class="{'show': showSelectDropdown}">
                    <li rel="hide">-- YCB OBJECT CLASS --</li>
                    <li v-for="(objectClass, i) in objectClasses"
                        :key="objectClass.displayName"
                        :rel="objectClass.value"
                        @click="pickObjectClass(i)">
                        {{ objectClass.displayName }}
                    </li>
                </ul>
            </div>
            <div class="file-upload-wrapper">
                <input type="file"
                       id="files"
                       class="custom-file-upload-hidden"
                       ref="files"
                       multiple
                       @change="handleUploadFiles()"/>
                <input type="text" class="file-upload-input" :title="fileNames" v-model="fileNames">
                <button class="select-files-button button" @click="triggerChangeOnFilesInput">SELECT FILES</button>
            </div>
            <button class="file-upload-button button" @click="submitFiles" :disabled="submitDisabled">SUBMIT FILES</button>
        </div>
    </section>
</template>

<script>
const objectClassDefault = '-- YCB OBJECT CLASS --';
export default {
    name: "FileUpload",
    data() {
        return {
            files: [],
            heading: 'Upload your files!',
            objectClasses: [
                { displayName: '011_banana', value: '10' },
                { displayName: '021_bleach_cleanser', value: '12' },
                { displayName: '035_power_drill', value: '15' },
                { displayName: '037_scissors', value: '17' }
            ],
            chosenObjectClass: objectClassDefault,
            showSelectDropdown: false
        }
    },
    computed: {
        filesSelected() {
            return this.files.length > 0
        },
        fileNames() {
            return this.filesSelected ? Array.from(this.files).map(file => file.name).join('; ') : ''
        },
        submitDisabled() {
            return this.chosenObjectClass === objectClassDefault || !this.filesSelected;
        }
    },
    methods: {
        pickObjectClass(index) {
            this.chosenObjectClass = this.objectClasses[index];
            this.toggleShowSelectDropdown();
        },
        toggleShowSelectDropdown() {
            this.showSelectDropdown = !this.showSelectDropdown
        },
        triggerChangeOnFilesInput() {
            this.$refs.files.click()
        },
        handleUploadFiles() {
            this.files = this.$refs.files.files;
        },
        submitFiles() {
            let formData = new FormData();
            this.files.forEach((file, i) => formData.append('files[' + i + ']', file));
            formData.append('objectClass', JSON.stringify(this.chosenObjectClass));
            this.$http.post('http://localhost:5000/upload-files',
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
                this.$emit('pointCloudUrlsReceived', response.data)
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

<style scoped lang="scss">
.show {
    display: block;
}

</style>