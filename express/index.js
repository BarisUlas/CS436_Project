import express from "express";
import mongoDBConnect from "./mongo/connect.js";
import mongoose from "mongoose";
import bodyParser from "body-parser";
import cors from "cors";
import userRoutes from "./routes/user.js";
import chatRoutes from "./routes/chat.js";
import messageRoutes from "./routes/message.js";
import User from "./models/userModel.js";

const app = express();

const PORT = process.env.EXPRESS_PORT;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());
app.use("/", userRoutes);
app.use("/api/chat", chatRoutes);
app.use("/api/message", messageRoutes);
mongoose.set("strictQuery", false);
mongoDBConnect();

app.listen(PORT, () => {
  console.log("creating chatbot user");
  const newuser = new User({ email: "chatbot@gmail.com", password: "password", name: "Chat Bot" });
  newuser.save();
  console.log(`Server Listening at PORT - ${PORT}`);
});
