import axios from "axios";

const sendMessageToChatBot = async (action, image=null) => {
    let reqData = {action};
    if (action !== "help") {
        reqData.image = image;
    }
    const {data} =await axios.post("https://us-central1-alpine-guild-417209.cloudfunctions.net/chat-bot", reqData);
    return data;
}

export {sendMessageToChatBot}