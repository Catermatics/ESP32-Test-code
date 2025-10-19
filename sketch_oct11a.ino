#define RELAY_1 4
#define RELAY_2 5
#define RELAY_3 6
#define RELAY_4 7
#define RELAY_5 15
#define RELAY_6 16
#define RELAY_7 17
#define RELAY_8 18
#define TRIG_PIN 13 // SR04
#define ECHO_PIN 14 // SR04
#define LDR_PIN 12  // MH光敏（類比腳）

void setup() {
  Serial.begin(115200);
  for (int i = RELAY_1; i <= RELAY_8; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    // 控制繼電器
    if (cmd.startsWith("RELAY")) {
      int index = cmd.substring(6,7).toInt();
      int val = cmd.substring(8,9).toInt();
      if (index >=1 && index <=8) digitalWrite(RELAY_1 + index - 1, val);
      Serial.println("OK");
    }
    // 讀SR04
    else if (cmd == "GET_DIST") {
      digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
      digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(TRIG_PIN, LOW);
      long duration = pulseIn(ECHO_PIN, HIGH);
      float distanceCm = duration * 0.034 / 2;
      Serial.println(distanceCm);
    }
    // 讀光感
    else if (cmd == "GET_LDR") {
      int ldrValue = analogRead(LDR_PIN);
      Serial.println(ldrValue);
    }
  }
}
