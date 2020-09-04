<template>
    <div></div>
</template>

<script>
import {Color, PerspectiveCamera, Scene, WebGLRenderer, Vector3} from 'three'
import {PCDLoader} from 'three/examples/jsm/loaders/PCDLoader.js';
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls.js';

export default {
    name: 'PCDViewer',
    props: {
        pointCloudUrl: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            renderer: null,
            scene: null,
            camera: null,
            controls: null
        }
    },
    methods: {
        loadPointCloud() {
            const loader = new PCDLoader();
            loader.load(this.pointCloudUrl,
                (points) => {
                    console.log("Successfully loaded point cloud.");
                    this.scene.add(points);
                    // fitCameraToObject(this.camera, points);
                    this.renderer.render( this.scene, this.camera );
                    const center = points.geometry.boundingSphere.center;
                    this.controls.target.set( center.x, center.y, center.z );
                    this.controls.update();
                },
                (xhr) => {
                    console.log(xhr + "Loading");
                },
                (error) => {
                    console.log(error + "Error");
                });
            let container = document.createElement('div');
            document.body.appendChild(container);
            container.appendChild(this.renderer.domElement);
            this.addControls();
            this.animate();
        },
        addControls() {
            this.controls = new TrackballControls( this.camera, this.renderer.domElement );
            this.controls.rotateSpeed = 2.0;
            this.controls.zoomSpeed = 0.3;
            this.controls.panSpeed = 0.2;
            this.controls.staticMoving = true;
        },
        initScene () {
            this.scene = new Scene();
            this.scene.background = new Color('black');
            this.camera = new PerspectiveCamera(20, window.innerWidth / window.innerHeight, 1, 1000);
            this.camera.position.set(0.3, 1, 1);
            this.camera.lookAt(new Vector3(0,0,0))
            this.scene.add(this.camera);
            this.renderer = new WebGLRenderer({antialias: true});
            this.renderer.setPixelRatio(window.devicePixelRatio);
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        },
        animate() {
            requestAnimationFrame( this.animate );
            this.controls.update();
            this.renderer.render( this.scene, this.camera );
        },
    },
    mounted() {
        this.initScene();
        this.loadPointCloud()
    }
}
</script>