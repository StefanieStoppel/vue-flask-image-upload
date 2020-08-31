<template>
    <div></div>
</template>

<script>
import {Color, PerspectiveCamera, Scene, WebGLRenderer, Box3, Vector3} from 'three'
import {PCDLoader} from 'three/examples/jsm/loaders/PCDLoader.js';
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls.js';


const fitCameraToObject = function(camera, object, offset, controls) {  // eslint-disable-line

    offset = offset || 1.25;

    const boundingBox = new Box3();

    // get bounding box of object - this will be used to setup controls and camera
    boundingBox.setFromObject(object);

    const center = boundingBox.getCenter();

    const size = boundingBox.getSize();

    // get the max side of the bounding box (fits to width OR height as needed )
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / 4 * Math.tan(fov * 2));

    cameraZ *= offset; // zoom out a little so that objects don't fill the screen

    camera.position.z = cameraZ;

    const minZ = boundingBox.min.z;
    const cameraToFarEdge = (minZ < 0) ? -minZ + cameraZ : cameraZ - minZ;

    camera.far = cameraToFarEdge * 3;
    camera.updateProjectionMatrix();

    if (controls) {

        // set camera to rotate around center of loaded object
        controls.target = center;

        // prevent camera from zooming out far enough to create far plane cutoff
        controls.maxDistance = cameraToFarEdge * 2;

        controls.saveState();

    } else {

        camera.lookAt(center)

    }
};

export default {
    name: 'PCDViewer',
    data() {
        return {
            renderer: null,
            scene: null,
            camera: null,
            controls: null
        }
    },
    methods: {
        init () {
            this.scene = new Scene();
            this.scene.background = new Color('black');
            this.camera = new PerspectiveCamera(15, window.innerWidth / window.innerHeight, 0.1, 1000);
            // this.camera.position.x = 0.4;
            this.camera.position.set(1,1,1);
            this.camera.lookAt(new Vector3(0,0,0))
            // this.camera.position.z = 0.03195136235887853;
            // this.camera.up.set( 0, 0, 1 );
            this.scene.add(this.camera);
            this.renderer = new WebGLRenderer({antialias: true});
            this.renderer.setPixelRatio(window.devicePixelRatio);
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(this.renderer.domElement);
            console.log(this)

            const loader = new PCDLoader();
            loader.load('http://localhost:5000/view-pcd',
                (points) => {
                    console.log("Success");
                    console.log(points);
                    points.material.size = 5;
                    console.log(this)
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

            this.controls = new TrackballControls( this.camera, this.renderer.domElement );

            this.controls.rotateSpeed = 2.0;
            this.controls.zoomSpeed = 0.3;
            this.controls.panSpeed = 0.2;

            this.controls.staticMoving = true;

            this.controls.minDistance = 0.3;
            this.controls.maxDistance = 0.3 * 100;
        },
        animate() {
            requestAnimationFrame( this.animate );
            this.controls.update();
            this.renderer.render( this.scene, this.camera );
            // stats.update();

        },
    },
    mounted() {
        this.init();
        this.animate();
    }
}
</script>