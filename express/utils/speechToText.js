import speech from '@google-cloud/speech';

// Creates a client
const client = new speech.SpeechClient({
    projectId: "cloudprojtrial",
    keyFilename: "key.json",
});

const sendAudioToSpeechToText = async (uri) => {
   const req = {
    config: {
        encoding: "MP3",
        sampleRateHertz: 16000,
        languageCode: "tr-TR",
        enableWordTimeOffsets: false
    },
    audio: {
        uri
    }
  };

  const [response] = await client.recognize(req);
  const transcription = response.results
    .map(result => result.alternatives[0].transcript)
    .join('\n');
return transcription;
}

export {sendAudioToSpeechToText};