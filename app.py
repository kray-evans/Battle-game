import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="JoJo Bizarre Fighting Game", page_icon="⭐", layout="centered")

st.title("⭐ JoJo's Bizarre Adventure: 2D Battle")
st.markdown("Trận chiến đỉnh cao giữa **Jotaro Kujo** và **DIO**! Sử dụng các nút điều khiển bên dưới hoặc bàn phím để tung đòn **ORA ORA / MUDA MUDA**.")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #0b0c10;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
            border-radius: 12px;
            overflow: hidden;
            border: 3px solid #c5a059;
        }
        canvas {
            background: linear-gradient(to bottom, #1f2833, #0b0c10);
            display: block;
        }
        .controls {
            margin-top: 10px;
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        button {
            padding: 12px 20px;
            font-size: 15px;
            font-weight: bold;
            background: linear-gradient(135deg, #c5a059, #f3e5ab);
            color: #111;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(197, 160, 89, 0.4);
            user-select: none;
            -webkit-user-select: none;
        }
        button:active {
            transform: scale(0.95);
            background: #fff;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="700" height="400"></canvas>
    </div>
    
    <div class="controls">
        <button id="leftBtn">◀ TRÁI</button>
        <button id="rightBtn">PHẢI ▶</button>
        <button id="jumpBtn">🡡 NHẢY</button>
        <button id="punchBtn">💥 ĐẤM (ORA)</button>
        <button id="specialBtn">⚡ TUYỆT KỸ</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Trạng thái game
        let gameOver = false;
        let winnerText = "";
        let screenShake = 0;

        // Nhân vật Player 1 (Jotaro)
        let p1 = {
            name: "JOTARO",
            x: 120,
            y: 270,
            width: 50,
            height: 90,
            color: "#1f4068",
            hp: 100,
            maxHp: 100,
            energy: 0,
            vx: 0,
            vy: 0,
            isJumping: false,
            isAttacking: false,
            attackTimer: 0,
            facing: "right"
        };

        // Nhân vật Player 2 / CPU (DIO)
        let p2 = {
            name: "DIO",
            x: 520,
            y: 270,
            width: 50,
            height: 90,
            color: "#e43f5a",
            hp: 100,
            maxHp: 100,
            energy: 0,
            vx: 0,
            vy: 0,
            isJumping: false,
            isAttacking: false,
            attackTimer: 0,
            facing: "left"
        };

        let keys = {};
        window.addEventListener("keydown", (e) => { keys[e.key] = true; });
        window.addEventListener("keyup", (e) => { keys[e.key] = false; });

        // Xử lý nút bấm di động
        const bindButton = (id, actionStart, actionEnd) => {
            const btn = document.getElementById(id);
            btn.addEventListener("mousedown", actionStart);
            btn.addEventListener("mouseup", actionEnd);
            btn.addEventListener("touchstart", (e) => { e.preventDefault(); actionStart(); });
            btn.addEventListener("touchend", (e) => { e.preventDefault(); actionEnd(); });
        };

        let mobileMoveLeft = false;
        let mobileMoveRight = false;

        bindButton("leftBtn", () => mobileMoveLeft = true, () => mobileMoveLeft = false);
        bindButton("rightBtn", () => mobileMoveRight = true, () => mobileMoveRight = false);
        bindButton("jumpBtn", () => { if (!p1.isJumping) { p1.vy = -12; p1.isJumping = true; } }, () => {});
        bindButton("punchBtn", () => triggerAttack(p1, p2, "ORA ORA!"), () => {});
        bindButton("specialBtn", () => triggerSpecial(p1, p2), () => {});

        function triggerAttack(attacker, defender, shout) {
            if (attacker.isAttacking || gameOver) return;
            attacker.isAttacking = true;
            attacker.attackTimer = 15;
            
            // Kiểm tra khoảng cách đánh trúng
            let dist = Math.abs((attacker.x + attacker.width/2) - (defender.x + defender.width/2));
            if (dist < 100) {
                defender.hp -= 12;
                attacker.energy = Math.min(100, attacker.energy + 20);
                screenShake = 10;
                
                // Hiệu ứng chữ kêu tên chiêu thức
                floatingText = { text: shout, x: defender.x, y: defender.y - 20, alpha: 1.0 };
            }
        }

        function triggerSpecial(attacker, defender) {
            if (attacker.energy < 100 || gameOver) return;
            attacker.energy = 0;
            defender.hp -= 35;
            screenShake = 25;
            floatingText = { text: "STAR PLATINUM: THE WORLD!", x: canvas.width/2 - 100, y: 100, alpha: 1.5 };
        }

        let floatingText = null;

        // AI điều khiển DIO đơn giản
        let aiTimer = 0;
        function updateAI() {
            if (gameOver) return;
            aiTimer++;
            
            let dist = p1.x - p2.x;
            if (Math.abs(dist) > 80) {
                p2.x += dist > 0 ? 2 : -2;
                p2.facing = dist > 0 ? "right" : "left";
            } else if (aiTimer % 40 === 0 && Math.random() < 0.7) {
                triggerAttack(p2, p1, "MUDA MUDA!");
            }
        }

        function update() {
            if (gameOver) return;

            // Điều khiển P1 (Jotaro) qua bàn phím
            if (keys["ArrowLeft"] || keys["a"] || mobileMoveLeft) {
                p1.x -= 4;
                p1.facing = "left";
            }
            if (keys["ArrowRight"] || keys["d"] || mobileMoveRight) {
                p1.x += 4;
                p1.facing = "right";
            }
            if ((keys["ArrowUp"] || keys["w"]) && !p1.isJumping) {
                p1.vy = -12;
                p1.isJumping = true;
            }
            if (keys[" "] && !p1.isAttacking) {
                triggerAttack(p1, p2, "ORA!");
            }

            // Trọng lực P1 & P2
            p1.y += p1.vy;
            p1.vy += 0.6;
            if (p1.y > 270) { p1.y = 270; p1.vy = 0; p1.isJumping = false; }

            p2.y += p2.vy;
            p2.vy += 0.6;
            if (p2.y > 270) { p2.y = 270; p2.vy = 0; p2.isJumping = false; }

            // Giới hạn biên màn hình
            p1.x = Math.max(20, Math.min(canvas.width - 70, p1.x));
            p2.x = Math.max(20, Math.min(canvas.width - 70, p2.x));

            if (p1.attackTimer > 0) p1.attackTimer--;
            if (p2.attackTimer > 0) p2.attackTimer--;

            updateAI();

            // Kiểm tra thắng thua
            if (p1.hp <= 0) {
                p1.hp = 0;
                gameOver = true;
                winnerText = "DIO THẮNG TRẬN!";
            } else if (p2.hp <= 0) {
                p2.hp = 0;
                gameOver = true;
                winnerText = "JOTARO THẮNG TRẬN!";
            }

            if (screenShake > 0) screenShake--;
        }

        function drawHUD() {
            // Thanh máu P1
            ctx.fillStyle = "#333";
            ctx.fillRect(30, 20, 250, 22);
            ctx.fillStyle = "#4ecc6d";
            ctx.fillRect(32, 22, (p1.hp / p1.maxHp) * 246, 18);
            ctx.fillStyle = "white";
            ctx.font = "bold 12px Arial";
            ctx.fillText(p1.name + " (" + p1.hp + "HP)", 40, 36);

            // Thanh năng lượng Stand P1
            ctx.fillStyle = "#333";
            ctx.fillRect(30, 48, 180, 10);
            ctx.fillStyle = "#f39c12";
            ctx.fillRect(32, 50, (p1.energy / 100) * 176, 6);

            // Thanh máu P2
            ctx.fillStyle = "#333";
            ctx.fillRect(420, 20, 250, 22);
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(422, 22, (p2.hp / p2.maxHp) * 246, 18);
            ctx.fillStyle = "white";
            ctx.fillText(p2.name + " (" + p2.hp + "HP)", 430, 36);
        }

        function drawFighter(f) {
            ctx.save();
            // Thân nhân vật
            ctx.fillStyle = f.color;
            ctx.fillRect(f.x, f.y, f.width, f.height);

            // Đầu nhân vật
            ctx.fillStyle = "#f1c27d";
            ctx.fillRect(f.x + 10, f.y - 15, 30, 20);

            // Hiệu ứng khi đang đánh (Tung đòn Stand)
            if (f.attackTimer > 0) {
                ctx.fillStyle = f === p1 ? "rgba(52, 152, 219, 0.6)" : "rgba(231, 76, 60, 0.6)";
                let punchX = f.facing === "right" ? f.x + f.width : f.x - 40;
                ctx.fillRect(punchX, f.y + 20, 40, 30);
            }
            ctx.restore();
        }

        function draw() {
            ctx.save();
            if (screenShake > 0) {
                let offsetX = (Math.random() - 0.5) * screenShake;
                let offsetY = (Math.random() - 0.5) * screenShake;
                ctx.translate(offsetX, offsetY);
            }

            // Vẽ sàn đấu
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#111";
            ctx.fillRect(0, 360, canvas.width, 40);
            ctx.fillStyle = "#c5a059";
            ctx.fillRect(0, 360, canvas.width, 4);

            drawFighter(p1);
            drawFighter(p2);
            drawHUD();

            // Hiệu ứng chữ bay
            if (floatingText) {
                ctx.fillStyle = "#f39c12";
                ctx.font = "bold 22px Arial";
                ctx.fillText(floatingText.text, floatingText.x, floatingText.y);
                floatingText.alpha -= 0.03;
                if (floatingText.alpha <= 0) floatingText = null;
            }

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#f3e5ab";
                ctx.font = "bold 35px Arial";
                ctx.textAlign = "center";
                ctx.fillText(winnerText, canvas.width / 2, canvas.height / 2 - 20);
                
                ctx.font = "16px Arial";
                ctx.fillStyle = "#fff";
                ctx.fillText("Tải lại trang (F5) để chơi lại ván mới", canvas.width / 2, canvas.height / 2 + 25);
                ctx.textAlign = "left";
            }

            ctx.restore();
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

components.html(game_code, height=480, scrolling=False)
nder.hp -= dmg;
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