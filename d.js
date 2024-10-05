// const { AudioContext } = require("node-web-audio-api");

// const audioContext = new AudioContext();

// // Create constant sound with harmonics and envelope for smoothness
// function createConstantSound(frequency = 440) {
//   const oscillator = audioContext.createOscillator();
//   const gainNode = audioContext.createGain();
//   const panNode = audioContext.createStereoPanner();

//   oscillator.type = "sine"; // You can change this to 'square', 'triangle', etc.
//   oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime); // Set frequency

//   // Set initial gain and pan values
//   gainNode.gain.setValueAtTime(1, audioContext.currentTime);
//   panNode.pan.setValueAtTime(0, audioContext.currentTime);

//   // Connect oscillator -> panNode -> gainNode -> destination (speakers)
//   oscillator.connect(panNode);
//   panNode.connect(gainNode);
//   gainNode.connect(audioContext.destination);

//   oscillator.start(); // Start sound immediately

//   return { oscillator, gainNode, panNode };
// }

// // Function to adjust pan and gain based on current angle
// function updateSpatialAudio(panNode, gainNode, angleInDegrees) {
//   // Convert angle to a normalized pan value (-1 to 1)
//   let panValue = Math.cos((angleInDegrees / 180) * Math.PI); // Maps from -1 (left) to 1 (right)
//   panNode.pan.setValueAtTime(panValue, audioContext.currentTime);

//   // Adjust gain based on angle (simulate distance or directionality)
//   let gainValue;
//   if (angleInDegrees < 45 || angleInDegrees > 315) {
//     gainValue = 1; // Full volume for front
//   } else if (angleInDegrees < 135) {
//     gainValue = 0.8; // Slightly reduced volume for right
//   } else if (angleInDegrees < 225) {
//     gainValue = 0.6; // Further reduced volume for back
//   } else {
//     gainValue = 0.8; // Slightly reduced volume for left
//   }
//   gainNode.gain.setValueAtTime(gainValue, audioContext.currentTime);
// }

// // Function to simulate a full 360-degree turn
// function simulateFullRotation() {
//   let currentAngle = 0; // Start at 0°
//   const turnStep = 5; // Define a small step for smooth turning

//   // Create the constant sound
//   const { panNode, gainNode } = createConstantSound(440);

//   const intervalId = setInterval(() => {
//     updateSpatialAudio(panNode, gainNode, currentAngle);

//     console.log(`Current Angle: ${currentAngle.toFixed(0)}°`);

//     // Increment angle to simulate turning
//     currentAngle = (currentAngle + turnStep) % 360; // Keep angle within 0-360°

//     if (currentAngle === 0) {
//       console.log(`Completed Full 360-Degree Turn`);
//     }
//   }, 100); // Smooth updates (100ms for real-time changes)
// }

// // Start the full 360-degree rotation simulation
// simulateFullRotation();

const { AudioContext } = require("node-web-audio-api");

const audioContext = new AudioContext();

// Create constant sound with harmonics and envelope for smoothness
function createBeepSound(frequency = 1000, duration = 0.2) {
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();

  oscillator.type = "sine"; // A pure sine wave beep
  oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime); // Beep frequency

  // Set initial gain and connect
  gainNode.gain.setValueAtTime(1, audioContext.currentTime);
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);

  oscillator.start(audioContext.currentTime);
  oscillator.stop(audioContext.currentTime + duration); // Play for specified duration
}

// Function to check if the current angle is within the target range
function isWithinTargetRange(currentAngle, targetAngle, range = 10) {
  const lowerBound = (targetAngle - range + 360) % 360;
  const upperBound = (targetAngle + range) % 360;

  if (lowerBound < upperBound) {
    return currentAngle >= lowerBound && currentAngle <= upperBound;
  } else {
    // For wraparound cases where the range crosses 0°
    return currentAngle >= lowerBound || currentAngle <= upperBound;
  }
}

// Function to simulate turning and check for beeping
function simulateTurnWithBeeping(targetAngle) {
  let currentAngle = 0; // Start at 0°
  const turnStep = 5; // Define step for smooth turning

  // Start rotating and checking conditions
  const intervalId = setInterval(() => {
    // Check if within target range (±10° of target)
    if (isWithinTargetRange(currentAngle, targetAngle, 10)) {
      createBeepSound(1000, 0.2); // Rapid beeps within target range
      console.log("Beep rapidly! In target range.");
    }

    // Check if 180° away from target (opposite direction)
    if (Math.abs(((currentAngle - targetAngle + 360) % 360) - 180) < 5) {
      createBeepSound(1000, 1); // Slow beeps when 180° away
      console.log("Beep slowly... Opposite direction.");
    }

    // Log current angle for reference
    console.log(`Current Angle: ${currentAngle.toFixed(0)}°`);

    // Increment angle to simulate turning
    currentAngle = (currentAngle + turnStep) % 360;

    if (currentAngle === 0) {
      console.log("Completed a Full 360° Turn");
    }
  }, 500); // Update every 500ms to match beeping pattern
}

// Set the target angle and simulate turning
simulateTurnWithBeeping(235);
