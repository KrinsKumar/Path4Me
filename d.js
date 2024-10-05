const { AudioContext } = require("node-web-audio-api");

const audioContext = new AudioContext();

function createSound(frequency = 440, duration = 2) {
  const sampleRate = audioContext.sampleRate;
  const audioBuffer = audioContext.createBuffer(
    1,
    sampleRate * duration,
    sampleRate
  );
  const data = audioBuffer.getChannelData(0);

  for (let i = 0; i < sampleRate * duration; i++) {
    data[i] = Math.sin(2 * Math.PI * frequency * (i / sampleRate));
  }

  return audioBuffer;
}

// Function to play spatial audio based on the given angle in degrees
// function playSpatialAudio(angleInDegrees) {
//   const sound = createSound();

//   const source = audioContext.createBufferSource(); // Create a source for playing the audio buffer
//   source.buffer = sound;

//   const panNode = audioContext.createStereoPanner();
//   const gainNode = audioContext.createGain();

//   let panValue = 1; // Normalize pan value between -1 and 1 based on the angle

//   // Set the pan value to position the sound in the stereo field based on the angle
//   panNode.pan.value = panValue;

//   // Adjust gain (volume) based on the angle, to simulate the direction of sound:
//   let gainValue = 1; // Default full volume

//   //   if (angleInDegrees < 45 || angleInDegrees > 315) {
//   //     // Front area (angle is between 0°-45° or 315°-360°)
//   //     gainValue = 0.4; // Lower volume for front
//   //   } else if (angleInDegrees < 135) {
//   //     // Right area (angle between 45°-135°)
//   //     gainValue = 0.5; // Slightly reduced volume for right
//   //   } else if (angleInDegrees < 225) {
//   //     // Back area (angle between 135°-225°)
//   //     gainValue = 0.6; // Further reduced volume for back
//   //   } else if (angleInDegrees < 315) {
//   //     // Left area (angle between 225°-315°)
//   //     gainValue = 0.3; // Lower volume for left
//   //   }

//   // Set the calculated gain value (volume adjustment) to the gain node
//   gainNode.gain.value = gainValue;

//   // Connect the audio nodes in the correct order:
//   // source -> panNode (adjust panning) -> gainNode (adjust volume) -> destination (speakers)
//   source.connect(panNode);
//   panNode.connect(gainNode);
//   gainNode.connect(audioContext.destination);

//   // Start playing the sound immediately
//   source.start();
// }
function playSpatialAudio(angleInDegrees) {
  const sound = createSound();

  const source = audioContext.createBufferSource(); // Create a source for playing the audio buffer
  source.buffer = sound;

  const panNode = audioContext.createStereoPanner();
  const gainNode = audioContext.createGain();

  // Convert angle to a normalized pan value (-1 to 1, where -1 is left and 1 is right)
  let panValue;
  if (angleInDegrees <= 90 || angleInDegrees >= 270) {
    // Sound is on the right or front
    panValue = Math.cos((angleInDegrees / 180) * Math.PI); // Range from 1 (front) to 0 (side) to -1 (back)
  } else {
    // Sound is on the left
    panValue = Math.cos(((360 - angleInDegrees) / 180) * Math.PI);
  }

  panNode.pan.value = panValue;

  // Adjust gain based on the angle to simulate distance/volume changes
  let gainValue;
  if (angleInDegrees < 45 || angleInDegrees > 315) {
    // Front area (angle is between 0°-45° or 315°-360°)
    gainValue = 1; // Full volume for front
  } else if (angleInDegrees < 135) {
    // Right area (angle between 45°-135°)
    gainValue = 0.8; // Slightly reduced volume for right
  } else if (angleInDegrees < 225) {
    // Back area (angle between 135°-225°)
    gainValue = 0.6; // Further reduced volume for back
  } else {
    // Left area (angle between 225°-315°)
    gainValue = 0.8; // Slightly reduced volume for left
  }

  gainNode.gain.value = gainValue;

  // Connect the audio nodes in the correct order:
  // source -> panNode (adjust panning) -> gainNode (adjust volume) -> destination (speakers)
  source.connect(panNode);
  panNode.connect(gainNode);
  gainNode.connect(audioContext.destination);

  // Start playing the sound immediately
  source.start();
}

// Function to simulate user turning towards a target angle
function simulateUserTurning(targetAngle) {
  let currentAngle = 0; // Start at 0°
  const turnStep = 5; // Define a small step for smooth turning

  const intervalId = setInterval(() => {
    playSpatialAudio(currentAngle);

    const clockwiseDistance = (targetAngle - currentAngle + 360) % 360;
    const counterClockwiseDistance = (currentAngle - targetAngle + 360) % 360;

    let turnDirection = "";
    let degreesRemaining = 0;

    if (clockwiseDistance <= counterClockwiseDistance) {
      turnDirection = "↻ Turn Right";
      degreesRemaining = clockwiseDistance;
      currentAngle = (currentAngle + turnStep) % 360;
    } else {
      turnDirection = "↺ Turn Left";
      degreesRemaining = counterClockwiseDistance;
      currentAngle = (currentAngle - turnStep + 360) % 360;
    }

    console.log(
      `Current Angle: ${currentAngle.toFixed(
        0
      )}° | Target Angle: ${targetAngle}° | ${turnDirection} (${degreesRemaining.toFixed(
        0
      )}°)`
    );

    if (Math.abs(currentAngle - targetAngle) < turnStep) {
      currentAngle = targetAngle;
      console.log(`Reached Target Angle: ${targetAngle}°`);
      clearInterval(intervalId);
    }
  }, 1000);
}

simulateUserTurning(235);
