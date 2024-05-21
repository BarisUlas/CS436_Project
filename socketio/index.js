const Server = require("socket.io");
const { createServer } = require("http");

const server = createServer();

const PORT = process.env.SOCKET_IO_PORT;
const ORIGIN = process.env.FRONTEND_BASE_URL;

console.log(PORT, ORIGIN);

const io = new Server.Server(server, {
  pingTimeout: 60000,
  cors: {
    origin: ORIGIN,
  },
});

io.on("connection", (socket) => {
  socket.on("setup", (userData) => {
    socket.join(userData.id);
    socket.emit("connected");
  });
  socket.on("join room", (room) => {
    socket.join(room);
  });
  socket.on("typing", (room) => socket.in(room).emit("typing"));
  socket.on("stop typing", (room) => socket.in(room).emit("stop typing"));

  socket.on("new message", (newMessageRecieve) => {
    var chat = newMessageRecieve.chatId;
    if (!chat.users) console.log("chats.users is not defined");
    chat.users.forEach((user) => {
      if (user._id == newMessageRecieve.sender._id) return;
      socket.in(user._id).emit("message recieved", newMessageRecieve);
    });
  });
});

server.listen(PORT);
