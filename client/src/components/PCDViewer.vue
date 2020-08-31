<template>
<div></div>
</template>

<script>
import {Color, PerspectiveCamera, Scene, WebGLRenderer} from 'three'
import { PCDLoader } from 'three/examples/jsm/loaders/PCDLoader.js';

export default {
  name: 'PCDViewer',
  data () {
    return {
      renderer: null,
      scene: null,
      camera: null,
      controls: null
    }
  },
  methods: {
    init: function () {
    this.scene = new Scene();
    this.scene.background = new Color( 0x000000 );
    this.camera = new PerspectiveCamera( 15, window.innerWidth / window.innerHeight, 0.1, 1000 );
    this.camera.position.z = 700;
    //this.camera.up.set( 0, 0, 1 );
    this.scene.add( this.camera );
    this.renderer = new WebGLRenderer( { antialias: true } );
    this.renderer.setPixelRatio( window.devicePixelRatio );
    this.renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( this.renderer.domElement );

    var loader = new PCDLoader();
    loader.load( 'http://localhost:5000/view-pcd',
    function ( points ) {
    points.material.size = 5;
    this.scene.add( points );
    });
    let container = document.createElement( 'div' );
    document.body.appendChild( container );
    container.appendChild( this.renderer.domElement );

    //this.scene = new Scene();
    //this.scene.background = new Color( 0x000000 );
    //this.camera = new PerspectiveCamera( 15, window.innerWidth / window.innerHeight, 0.1, 1000 );
    //this.camera.position.z = 700;
    //this.scene.add( this.camera );
    //this.renderer = new WebGLRenderer( { antialias: true } );
    //this.renderer.setPixelRatio( window.devicePixelRatio );
    //this.renderer.setSize( window.innerWidth, window.innerHeight );
    //document.body.appendChild( this.renderer.domElement );
    //var loader = new PCDLoader();
    //loader.load('/Users/aleksandrakornivec/vue-flask-image-upload/client/src/assets/test-completed.pcd',
    //function ( points ) {
    //points.material.size = 5;
    //this.scene.add( points );});
    //let container = document.createElement( 'div' );
    //document.body.appendChild( container );
    //container.appendChild( this.renderer.domElement );
    }
  },
  mounted () {
    this.init()
  }
}
</script>