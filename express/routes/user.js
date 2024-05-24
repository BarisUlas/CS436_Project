import express from "express";
import {
  register,
  login,
  validUser,
  googleAuth,
  logout,
  searchUsers,
  updateInfo,
  getUserById,
} from "../controllers/user.js";
import { Auth } from "../middleware/user.js";
const router = express.Router();
router.post("/api/auth/register", register);
router.post("/api/auth/login", login);
router.get("/api/auth/valid", Auth, validUser);
router.get("/api/auth/logout", Auth, logout);
router.post("/api/google", googleAuth);
router.get("/api/user?", Auth, searchUsers);
router.get("/api/users/:id", Auth, getUserById);
router.patch("/api/users/update/:id", Auth, updateInfo);
export default router;
