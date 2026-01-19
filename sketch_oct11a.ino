// Define pins for all 17 relays as per your list
const int relayPins[] = {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
const int NUM_RELAYS = sizeof(relayPins) / sizeof(relayPins[0]);

void setup() {
  Serial.begin(115200);

  // Initialize all Relay pins using the array
  for (int i = 0; i < NUM_RELAYS; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], LOW); // Ensure they start OFF
  }
  Serial.println("System Ready. Send: RELAY <index> <state>");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("RELAY")) {
      // Use sscanf to safely parse multi-digit integers
      // Format expected: "RELAY 15 1"
      int index;
      int val;
      
      // sscanf returns the number of successfully parsed variables
      if (sscanf(cmd.c_str(), "RELAY %d %d", &index, &val) == 2) {
        
        // Check if index is within our valid range (1 to 16/17)
        if (index >= 1 && index <= NUM_RELAYS) {
          // Map index (1-based) to array (0-based)
          digitalWrite(relayPins[index - 1], val);
          
          Serial.print("OK: Relay ");
          Serial.print(index);
          Serial.println(val == 1 ? " ON" : " OFF");
        } else {
          Serial.println("Error: Index out of range");
        }
      } else {
        Serial.println("Error: Invalid Command Format. Use 'RELAY <num> <0/1>'");
      }
    }
  }
}
