import axios from "axios";
import { uploadToCloudStorage } from "./cloudStorage.js";

const sendMessageToChatBot = async (action, image=null) => {
    let reqData = {action};
    if (action !== "help") {
        reqData.image = image.split(",")[1];
    }
    const { data } = await axios.post("https://us-central1-alpine-guild-417209.cloudfunctions.net/chat-bot", reqData);
    if (action === "help") {
        return data;
    }
    return await uploadToCloudStorage(data, "png");
}

export { sendMessageToChatBot };