// audio.js

// Function to play audio
function playAudio(languageCode) {
    // Define the audio file URLs for each language code
    const audioFiles = {
        'en': 'audio_en.mp3',
        'ta': 'audio_ta.mp3',
        'te': 'audio_te.mp3',
        'kn': 'audio_kn.mp3',
        'ml': 'audio_ml.mp3',
    };

    // Get the audio element by its ID
    const audioElement = document.getElementById('audioPlayer');

    // Set the audio source based on the selected language code
    if (audioFiles.hasOwnProperty(languageCode)) {
        audioElement.src = audioFiles[languageCode];
    } else {
        // Handle the case where audio is not available for the selected language
        alert('Audio not available for the selected language.');
        return;
    }

    // Play the audio
    audioElement.play();
}
