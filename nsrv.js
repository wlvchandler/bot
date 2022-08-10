const mariadb = require('mariadb');
require('dotenv').config()

const pool = mariadb.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    connectionLimit: 5,
    database: process.env.DB_BASE
});

const { Server } = require("socket.io");

const io = new Server(8765, {
    cors: {
	origin: "https://jaskaa.com:8765",
	methods: ["GET", "POST"],
	allowedHeaders: ["Access-Control-Allow-Origin"]
    }
});


io.on("connection", (socket) => {
    console.log("event: connection");
    console.log(socket.id);

    function fixBigInt(data) {
        return JSON.parse(JSON.stringify(data, (key, value) =>
            typeof value === 'bigint'
                ? Number(value.toString())
                : value // return everything else unchanged
        ));
    }

    var conn = pool.getConnection();
    BLURSES = {'Bless':null, 'Curse':null};
    socket.on("updateBlurses", () => {
	console.log(BLURSES);
	conn.then(conn => {
	    //for (var bcType in BLURSES) {
	    Object.entries(BLURSES).forEach(([bcType,bcList]) => {
		console.log(`Gathering: ${bcType}`);
		console.log(`select user, count(*) as COUNT from blurse where type="${bcType}" group by user order by COUNT desc, user;`);
		conn.query(`select user, count(*) as COUNT from blurse where type="${bcType}" group by user order by COUNT desc, user;`)
		    .then((rows) => {
			console.log(`about to check ${bcType}s`);
			r = fixBigInt(rows);
			if (JSON.stringify(r) !== JSON.stringify(bcList)) {
			    console.log(r);
			    console.log(`Sending ${bcType}`);
			    socket.emit("rcv_Blurses", r, bcType);
			    BLURSES[bcType] = r;
			}
		    })
		    .catch(err => {
			console.log(err);
			conn.end();
		    })
		    .finally(() =>{
			console.log("Freeing connection");
			conn.end();
		    });
	    });
	    
	}).catch(err => {
	    console.log(err);
	});
    });
});

io.on("connect_error", (err) => {
    console.log("event: connection error");
    console.log("connection error");
});


