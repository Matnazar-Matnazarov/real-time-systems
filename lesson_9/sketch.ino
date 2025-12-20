#define LED_PIN 13

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

unsigned long lastBlink = 0;
unsigned long lastSerial = 0;

void loop() {
  unsigned long now = millis();

  if (now - lastBlink >= 1000) {
    static bool ledState = false;
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
    lastBlink = now;
  }

  if (now - lastSerial >= 2000) {
    Serial.println("Wokwi: multitasking simulation ishlayapti...");
    lastSerial = now;
  }
}
