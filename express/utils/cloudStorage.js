import { Storage} from "@google-cloud/storage";
import fs from "fs";

function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

const storage = new Storage({
  projectId: "cloudprojtrial",
  keyFilename: "key.json",
});

const uploadToCloudStorage = async (base64, extension) => {
    console.log('base 64 is.....')
    console.log(base64.substring(0,100));
    const buffer = Buffer.from(base64, "base64");
    const filename = `${makeid(10)}.${extension}`
    fs.writeFileSync(filename, buffer);

    try {
        const gcs = storage.bucket("msg_storage"); // Removed "gs://" from the bucket name
        const storagepath = `storage_folder/${filename}`;
        const result = await gcs.upload(filename, {
            destination: storagepath,
            predefinedAcl: 'publicRead', // Set the file to be publicly readable
        });
        return result[0].metadata.mediaLink;
    } catch (error) {
        console.log(error);
        throw new Error(error.message);
    }
}


export {uploadToCloudStorage}