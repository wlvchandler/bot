
function draw() {
    let socket = new WebSocket("wss://javascript.info");
}

//var alert_poll = setInterval(PollAlerts, 1000);

// function draw() {
//     var canvas = document.getElementById('tutorial');
//     var ctx = canvas.getContext('2d');

//     // canvas.width = window.innerWidth;
//     // canvas.height = window.innerHeight;
    
//     if (ctx) {
// 	var x = Math.floor(Math.random() * canvas.width);
// 	var y = Math.floor(Math.random() * canvas.height);
// 	var vx = Math.floor(Math.random() * 20);
// 	var vy = Math.floor(Math.random() * 40);
// 	var r = 200;
// 	move();

// 	function move() {
// 	    requestAnimationFrame(move);
// 	    ctx.clearRect(0,0, canvas.width, canvas.height);
	    
// 	    ctx.beginPath();
// 	    ctx.strokeStyle = "red";
// 	    ctx.arc(x,y,r, Math.PI * 2, false);
// 	    ctx.stroke();

// 	    if (x + r > innerWidth || x - r < 0) vx = 0-vx;
// 	    if (y + r > innerHeight|| y - r < 0) vy = 0-vy;
// 	    x = x + vx;
// 	    y = y + vy;
// 	}
//     }
// }


//window.main = draw;
