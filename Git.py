<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GTA Mobile AI Experiment</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; touch-action: none; }
        #hud { position: absolute; top: 10px; right: 10px; color: #5eff5e; font-family: monospace; font-size: 20px; text-shadow: 2px 2px #000; pointer-events: none; }
        
        /* Controles Táctiles */
        .touch-btn { 
            position: absolute; width: 70px; height: 70px; 
            background: rgba(255,255,255,0.2); border: 2px solid #fff; 
            border-radius: 50%; color: white; display: flex; 
            justify-content: center; align-items: center; font-weight: bold;
            user-select: none; -webkit-tap-highlight-color: transparent;
        }
        #btn-shoot { bottom: 40px; right: 40px; background: rgba(255, 0, 0, 0.4); }
        #btn-action { bottom: 130px; right: 40px; background: rgba(0, 0, 255, 0.4); }
        
        /* Joystick */
        #joystick-container { 
            position: absolute; bottom: 40px; left: 40px; 
            width: 120px; height: 120px; background: rgba(255,255,255,0.1); 
            border-radius: 50%; 
        }
        #joystick-knob { 
            position: absolute; top: 35px; left: 35px; 
            width: 50px; height: 50px; background: #fff; border-radius: 50%; 
        }
    </style>
</head>
<body>
    <div id="hud"> $00000350 </div>
    
    <div id="joystick-container">
        <div id="joystick-knob"></div>
    </div>
    <div id="btn-shoot" class="touch-btn">PUM</div>
    <div id="btn-action" class="touch-btn">F</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script>
        let scene, camera, renderer, player;
        let moveForward = false, moveBackward = false, turnLeft = false, turnRight = false;

        // Lógica de Joystick Táctil
        const knob = document.getElementById('joystick-knob');
        const container = document.getElementById('joystick-container');
        
        container.addEventListener('touchmove', (e) => {
            const touch = e.touches[0];
            const rect = container.getBoundingClientRect();
            const x = touch.clientX - rect.left - rect.width/2;
            const y = touch.clientY - rect.top - rect.height/2;
            
            // Limitar movimiento del knob
            const distance = Math.min(60, Math.sqrt(x*x + y*y));
            const angle = Math.atan2(y, x);
            
            knob.style.transform = `translate(${Math.cos(angle)*distance}px, ${Math.sin(angle)*distance}px)`;
            
            // Traducir a movimiento del juego
            moveForward = y < -20;
            moveBackward = y > 20;
            turnLeft = x < -20;
            turnRight = x > 20;
        });

        container.addEventListener('touchend', () => {
            knob.style.transform = `translate(0px, 0px)`;
            moveForward = moveBackward = turnLeft = turnRight = false;
        });

        // Botón de Disparo
        document.getElementById('btn-shoot').addEventListener('touchstart', (e) => {
            e.preventDefault();
            shoot();
        });

        function shoot() {
            const b = new THREE.Mesh(new THREE.SphereGeometry(0.1), new THREE.MeshBasicMaterial({color: 0xffff00}));
            b.position.copy(player.position).add(new THREE.Vector3(0, 1.2, 0));
            const dir = new THREE.Vector3(0,0,1).applyQuaternion(player.quaternion);
            scene.add(b);
            // Lógica de proyectil...
        }

        // --- MOTOR DE JUEGO (SIMPLIFICADO PARA MÓVIL) ---
        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87ceeb);
            camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
            renderer = new THREE.WebGLRenderer({ antialias: false }); // Antialias off para mejor FPS en móvil
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(window.devicePixelRatio > 1 ? 2 : 1); // Optimización de pantalla
            document.body.appendChild(renderer.domElement);

            // Suelo y Jugador
            const ground = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), new THREE.MeshStandardMaterial({color: 0x333333}));
            ground.rotation.x = -Math.PI/2;
            scene.add(ground);
            scene.add(new THREE.AmbientLight(0xffffff, 0.8));

            player = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.8, 0.4), new THREE.MeshStandardMaterial({color: 0x4b3621}));
            body.position.y = 0.9;
            player.add(body);
            scene.add(player);

            animate();
        }

        function animate() {
            requestAnimationFrame(animate);

            if(moveForward) player.translateZ(0.1);
            if(moveBackward) player.translateZ(-0.05);
            if(turnLeft) player.rotation.y += 0.04;
            if(turnRight) player.rotation.y -= 0.04;

            // Cámara sigue al jugador
            let offset = new THREE.Vector3(0, 2.5, -5).applyMatrix4(player.matrixWorld);
            camera.position.lerp(offset, 0.1);
            camera.lookAt(player.position.x, player.position.y + 1, player.position.z);

            renderer.render(scene, camera);
        }

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        init();
    </script>
</body>
</html>
