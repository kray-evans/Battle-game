```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="JoJo's Bizarre Adventure - 2D Fighter", page_icon="⭐", layout="centered")

st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #f1c40f; margin-bottom: 0;">⭐ JOJO'S BIZARRE ADVENTURE: BATTLE TIDE ⭐</h1>
    <p style="color: #bdc3c7; font-size: 15px;">Chọn nhân vật, triệu hồi Stand và tung đòn ORA ORA / MUDA MUDA!</p>
</div>
""", unsafe_allow_html=True)

jojo_game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JoJo 2D Fighter</title>
    <style>
        body {
            margin: 0;
            background: #0d0f18;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 40px rgba(241, 196, 15, 0.2);
            border-radius: 12px;
            overflow: hidden;
            border: 3px solid #f1c40f;
        }
        canvas {
            display: block;
            background: linear-gradient(180deg, #1b1e36 0%, #0d0f18 100%);
        }
        /* Màn hình Chọn Nhân vật */
        #char-select {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(13, 15, 24, 0.95);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }
        .char-grid {
            display: flex;
            gap: 30px;
            margin-top: 20px;
        }
        .char-card {
            width: 140px;
            height: 200px;
            border: 3px solid #4a69bd;
            border-radius: 10px;
            background: #1e272e;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .char-card:hover, .char-card.selected {
            border-color: #f1c40f;
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(241, 196, 15, 0.5);
        }
        /* Bảng điều khiển cảm ứng cho Mobile */
        .controls-container {
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
            width: 750px;
            max-width: 100%;
            padding: 0 10px;
            box-sizing: border-box;
        }
        .dpad, .action-pad {
            display: flex;
            gap: 8px;
        }
        .btn {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            border: none;
            padding: 12px 18px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .btn:active {
            transform: scale(0.95);
            background: #962d22;
        }
        .btn-blue {
            background: linear-gradient(135deg, #3498db, #2980b9);
        }
        .btn-yellow {
            background: linear-gradient(135deg, #f1c40f, #f39c12);
            color: #000;
        }
        .instructions {
            font-size: 11px;
            color: #95a5a6;
            margin-top: 6px;
            text-align: center;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <!-- MÀN HÌNH CHỌN NHÂN VẬT -->
        <div id="char-select">
            <h2 style="color: #f1c40f; text-shadow: 0 0 10px #f1c40f;">CHỌN ĐẤU SĨ CỦA BẠN</h2>
            <div class="char-grid">
                <div class="char-card" onclick="selectCharacter('jotaro')">
                    <div style="font-size: 40px;">⭐</div>
                    <h3 style="margin: 10px 0 5px 0; color: #3498db;">JOTARO</h3>
                    <p style="font-size: 12px; color: #bdc3c7; text-align: center;">Stand: Star Platinum</p>
                </div>
                <div class="char-card" onclick="selectCharacter('dio')">
                    <div style="font-size: 40px;">🌙</div>
                    <h3 style="margin: 10px 0 5px 0; color: #e74c3c;">DIO</h3>
                    <p style="font-size: 12px; color: #bdc3c7; text-align: center;">Stand: The World</p>
                </div>
            </div>
            <p style="margin-top: 30px; font-size: 13px; color: #f1c40f;">Bấm vào nhân vật để bắt đầu trận đấu!</p>
        </div>

        <canvas id="gameCanvas" width="750" height="400"></canvas>
    </div>

    <!-- NÚT ĐIỀU KHIỂN MOBILE -->
    <div class="controls-container">
        <div class="dpad">
            <button class="btn btn-blue" id="leftBtn">◀ TRÁI</button>
            <button class="btn btn-blue" id="rightBtn">PHẢI ▶</button>
            <button class="btn btn-blue" id="jumpBtn">▲ NHẢY</button>
        </div>
        <div class="action-pad">
            <button class="btn" id="atkBtn">ĐÁNH (J)</button>
            <button class="btn btn-yellow" id="specialBtn">STAND RUSH (K)</button>
            <button class="btn" style="background:#8e44ad;" id="ultBtn">ULTI (L)</button>
        </div>
    </div>
    <div class="instructions">PC: Dùng A/D hoặc Mũi tên để di chuyển, J (Đánh), K (Stand Rush), L (Ultimate)</div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let gameStarted = false;
        let playerChoice = 'jotaro';

        function selectCharacter(char) {
            playerChoice = char;
            document.getElementById("char-select").style.display = "none";
            initGame();
            gameStarted = true;
        }

        // Trạng thái game & Biến chiến đấu
        let player, enemy, particles = [], texts = [];
        let keys = {};

        class Fighter {
            constructor(x, y, isPlayer, name, color, standName) {
                this.x = x;
                this.y = y;
                this.width = 50;
                this.height = 100;
                this.vx = 0;
                this.vy = 0;
                this.isPlayer = isPlayer;
                this.name = name;
                this.color = color;
                this.standName = standName;
                
                this.hp = 100;
                this.maxHp = 100;
                this.standGauge = 0; // Tăng dần khi đánh trúng
                
                this.isJumping = false;
                this.isAttacking = false;
                this.attackTimer = 0;
                this.attackType = null;
                this.facing = isPlayer ? 1 : -1;
                this.stunTimer = 0;
                this.win = false;
            }

            update() {
                if (this.stunTimer > 0) {
                    this.stunTimer--;
                    return;
                }

                // Trọng lực
                this.vy += 0.5;
                this.y += this.vy;
                this.x += this.vx;

                // Sàn đấu
                if (this.y > 280) {
                    this.y = 280;
                    this.vy = 0;
                    this.isJumping = false;
                }

                // Giới hạn biên màn hình
                if (this.x < 20) this.x = 20;
                if (this.x > canvas.width - 70) this.x = canvas.width - 70;

                // Giảm tốc độ trượt
                this.vx *= 0.8;

                if (this.attackTimer > 0) {
                    this.attackTimer--;
                    if (this.attackTimer === 0) this.isAttacking = false;
                }
            }

            draw() {
                ctx.save();
                // Vẽ bóng nhân vật
                ctx.fillStyle = "rgba(0,0,0,0.3)";
                ctx.beginPath();
                ctx.ellipse(this.x + this.width/2, 380, 25, 8, 0, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ thân nhân vật chính
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);

                // Mũ / Tóc đặc trưng
                ctx.fillStyle = "#111";
                if (this.name === "JOTARO") {
                    ctx.fillRect(this.x + (this.facing > 0 ? 20 : 0), this.y, 30, 25);
                } else {
                    // Tóc vàng DIO
                    ctx.fillStyle = "#f1c40f";
                    ctx.fillRect(this.x + 5, this.y - 10, 40, 20);
                }

                // Vẽ hiệu ứng Stand nếu đang tấn công đặc biệt
                if (this.isAttacking && this.attackType === 'special') {
                    ctx.fillStyle = this.name === "JOTARO" ? "rgba(52, 152, 219, 0.7)" : "rgba(241, 196, 15, 0.7)";
                    let standX = this.facing > 0 ? this.x + 50 : this.x - 70;
                    ctx.fillRect(standX, this.y - 20, 70, 120);
                }

                ctx.restore();
            }

            attack(type) {
                if (this.isAttacking || this.stunTimer > 0) return;
                this.isAttacking = true;
                this.attackType = type;

                if (type === 'normal') {
                    this.attackTimer = 15;
                    checkHit(this, 15, 10, 'normal');
                } else if (type === 'special') {
                    this.attackTimer = 35;
                    checkHit(this, 35, 25, 'special');
                    spawnShoutText(this.x, this.y - 30, this.name === "JOTARO" ? "ORA ORA ORA!" : "MUDA MUDA MUDA!", this.color);
                } else if (type === 'ult' && this.standGauge >= 100) {
                    this.attackTimer = 50;
                    this.standGauge = 0;
                    checkHit(this, 50, 45, 'ult');
                    spawnShoutText(canvas.width / 2 - 100, 150, this.name === "JOTARO" ? "STAR PLATINUM: THE WORLD!" : "THE WORLD: TOKI WO TOMARE!", "#e74c3c");
                }
            }
        }

        function initGame() {
            let pColor = playerChoice === 'jotaro' ? '#2980b9' : '#c0392b';
            let eColor = playerChoice === 'jotaro' ? '#c0392b' : '#2980b9';
            let pName = playerChoice === 'jotaro' ? 'JOTARO' : 'DIO';
            let eName = playerChoice === 'jotaro' ? 'DIO' : 'JOTARO';

            player = new Fighter(150, 280, true, pName, pColor, pName === 'JOTARO' ? 'Star Platinum' : 'The World');
            enemy = new Fighter(550, 280, false, eName, eColor, eName === 'JOTARO' ? 'Star Platinum' : 'The World');
            particles = [];
            texts = [];
        }

        function checkHit(attacker, range, dmg, type) {
            let defender = attacker.isPlayer ? enemy : player;
            let distance = Math.abs((attacker.x + attacker.width/2) - (defender.x + defender.width/2));
            
            if (distance < 90 + (type === 'ult' ? 50 : 0)) {
                defender.hp -= dmg;
                defender.stunTimer = 15;
                defender.vx = attacker.facing * (type === 'ult' ? 12 : 6);
                defender.vy = -4;

                attacker.standGauge = Math.min(100, attacker.standGauge + (type === 'normal' ? 15 : 40));

                // Tạo hiệu ứng tia lửa va chạm
                for (let i = 0; i < 10; i++) {
                    particles.push({
                        x: defender.x + defender.width/2,
                        y: defender.y + defender.height/2,
                        vx: (Math.random() - 0.5) * 10,
                        vy: (Math.random() - 0.5) * 10,
                        color: '#f1c40f',
                        life: 20
                    });
                }
            }
        }

        function spawnShoutText(x, y, text, color) {
            texts.push({ x: x, y: y, text: text, color: color, life: 40 });
        }

        // AI điều khiển đối thủ đơn giản
        function updateAI() {
            if (enemy.hp <= 0 || player.hp <= 0) return;
            
            let dx = player.x - enemy.x;
            if (Math.abs(dx) > 70) {
                enemy.vx = dx > 0 ? 2 : -2;
                enemy.facing = dx > 0 ? 1 : -1;
            } else {
                if (Math.random() < 0.05) {
                    if (enemy.standGauge >= 100 && Math.random() < 0.3) {
                        enemy.attack('ult');
                    } else if (Math.random() < 0.6) {
                        enemy.attack('special');
                    } else {
                        enemy.attack('normal');
                    }
                }
            }
        }

        // Bắt sự kiện bàn phím
        window.addEventListener("keydown", (e) => { keys[e.key.toLowerCase()] = true; });
        window.addEventListener("keyup", (e) => { keys[e.key.toLowerCase()] = false; });

        // Gán sự kiện nút cảm ứng mobile
        const bindButton = (id, action) => {
            const el = document.getElementById(id);
            if (!el) return;
            el.addEventListener("mousedown", action);
            el.addEventListener("touchstart", (e) => { e.preventDefault(); action(); });
        };

        bindButton("leftBtn", () => { player.vx = -5; player.facing = -1; });
        bindButton("rightBtn", () => { player.vx = 5; player.facing = 1; });
        bindButton("jumpBtn", () => { if (!player.isJumping) { player.vy = -11; player.isJumping = true; } });
        bindButton("atkBtn", () => { player.attack('normal'); });
        bindButton("specialBtn", () => { player.attack('special'); });
        bindButton("ultBtn", () => { player.attack('ult'); });

        function update() {
            if (!gameStarted) return;

            // Xử lý phím di chuyển PC
            if (keys["a"] || keys["arrowleft"]) { player.vx = -5; player.facing = -1; }
            if (keys["d"] || keys["arrowright"]) { player.vx = 5; player.facing = 1; }
            if ((keys["w"] || keys["arrowup"]) && !player.isJumping) { player.vy = -11; player.isJumping = true; }
            if (keys["j"]) { player.attack('normal'); }
            if (keys["k"]) { player.attack('special'); }
            if (keys["l"]) { player.attack('ult'); }

            player.update();
            updateAI();
            enemy.update();

            // Cập nhật hướng mặt đối đầu
            if (player.x < enemy.x) {
                player.facing = 1;
                enemy.facing = -1;
            } else {
                player.facing = -1;
                enemy.facing = 1;
            }

            // Cập nhật hạt hiệu ứng
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life--;
                if (p.life <= 0) particles.splice(i, 1);
            }

            // Cập nhật text hội thoại / shout
            for (let i = texts.length - 1; i >= 0; i--) {
                let t = texts[i];
                t.y -= 1;
                t.life--;
                if (t.life <= 0) texts.splice(i, 1);
            }
        }

        function drawUI() {
            // Thanh máu Người chơi
            ctx.fillStyle = "#333";
            ctx.fillRect(30, 20, 250, 22);
            ctx.fillStyle = "#2ecc71";
            ctx.fillRect(30, 20, (player.hp / player.maxHp) * 250, 22);
            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 2;
            ctx.strokeRect(30, 20, 250, 22);
            
            ctx.fillStyle = "#fff";
            ctx.font = "bold 14px Segoe UI";
            ctx.fillText(player.name + " (HP)", 35, 36);

            // Thanh Stand Gauge Người chơi
            ctx.fillStyle = "#333";
            ctx.fillRect(30, 48, 180, 12);
            ctx.fillStyle = "#f1c40f";
            ctx.fillRect(30, 48, (player.standGauge / 100) * 180, 12);
            ctx.strokeRect(30, 48, 180, 12);
            ctx.fillStyle = "#fff";
            ctx.font = "10px Segoe UI";
            ctx.fillText("STAND METER", 35, 58);

            // Thanh máu Đối thủ
            ctx.fillStyle = "#333";
            ctx.fillRect(470, 20, 250, 22);
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(470 + (250 - (enemy.hp / enemy.maxHp) * 250), 20, (enemy.hp / enemy.maxHp) * 250, 22);
            ctx.strokeRect(470, 20, 250, 22);
            
            ctx.fillStyle = "#fff";
            ctx.font = "bold 14px Segoe UI";
            ctx.fillText(enemy.name + " (HP)", 580, 36);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ nền đấu trường (Sân khấu Cairo / Thành phố)
            ctx.fillStyle = "#1e272e";
            ctx.fillRect(0, 280, canvas.width, 120);
            ctx.fillStyle = "#f1c40f";
            ctx.fillRect(0, 276, canvas.width, 4);

            if (!gameStarted) return;

            player.draw();
            enemy.draw();

            // Vẽ hạt hiệu ứng va chạm
            for (let p of particles) {
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 4, 4);
            }

            // Vẽ text shouts (ORA ORA / MUDA MUDA)
            for (let t of texts) {
                ctx.save();
                ctx.font = "bold 22px Impact";
                ctx.fillStyle = t.color;
                ctx.shadowColor = "#000";
                ctx.shadowBlur = 6;
                ctx.fillText(t.text, t.x, t.y);
                ctx.restore();
            }

            drawUI();

            // Kiểm tra thắng thua
            if (player.hp <= 0 || enemy.hp <= 0) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = player.hp <= 0 ? "#e74c3c" : "#f1c40f";
                ctx.font = "bold 36px Segoe UI";
                ctx.textAlign = "center";
                ctx.fillText(player.hp <= 0 ? "BẠN ĐÃ THẤT BẠI!" : "CHIẾN THẮNG HUY HOÀNG!", canvas.width / 2, canvas.height / 2 - 20);

                ctx.fillStyle = "#fff";
                ctx.font = "16px Segoe UI";
                ctx.fillText("Bấm F5 hoặc tải lại trang để chơi trận mới", canvas.width / 2, canvas.height / 2 + 25);
                ctx.textAlign = "left";
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

components.html(jojo_game_code, height=530, scrolling=False)
```