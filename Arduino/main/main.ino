#include <FastLED.h>

#define NUM_LEDS      42
#define DATA_PIN      11
#define CLOCK_PIN     13
#define INTERRUPT_PIN 2
#define MAX_DEGREE    180
#define IMAGE_SIZE    42

float last_rotation = 0;
float turn_start;
float current_turn;
int LAST_INDEX = 0;

CRGB leds[NUM_LEDS];

const int EXTRACTION_SIZE = 12;
CRGB picture[EXTRACTION_SIZE][IMAGE_SIZE] = {{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0)},{CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0)},{CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255)},{CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(255, 255, 255), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(0, 0, 0), CRGB(255, 255, 255), CRGB(255, 255, 255)}};

void LED_test(){
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB::White;
    FastLED.show();
    delay(10);
    leds[i] = CRGB::Black;
  }
  for(int i = NUM_LEDS-1; i >= 0; i--){
    leds[i] = CRGB::White;
    FastLED.show();
    delay(10);
    leds[i] = CRGB::Black;
  }
  for(int j = 0; j < EXTRACTION_SIZE; j++) {
    for(int i = 0; i < NUM_LEDS; i++) leds[i] = picture[j][i];
    FastLED.show();
    delay(100);
  }
  for(int i = 0; i < NUM_LEDS; i++) leds[i] = CRGB::Black;
  FastLED.show();
}

void drawPicture(float degree){
  // degree = 1 => 360°
  if(degree > 1) degree = 1;
  int index = round(degree * EXTRACTION_SIZE * 2);

  // 360° = 1 * EXTRACTION_SIZE * 2 = EXTRACTION_SIZE * 2 => 0
  while(index >= EXTRACTION_SIZE) index -= EXTRACTION_SIZE;

  // If we're already showing the correct image, skip
  if(index == LAST_INDEX) return;
  // Otherwise, register the current image's index.
  LAST_INDEX = index;

  // 0 <= degree < 180
  if(degree < 0.5) for(int i = 0; i < NUM_LEDS; i++) leds[i] = picture[index][i];

  // 180 <= degree < 360
  else for(int i = 0; i < NUM_LEDS; i++) leds[i] = picture[index][NUM_LEDS - 1 - i];
  
  FastLED.show();
}

void oneTurn(){
  turn_start = (float) millis();
  last_rotation = current_turn;
  current_turn = 0;
}

void setup() {
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, GBR>(leds, NUM_LEDS);
  FastLED.setBrightness(3);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), oneTurn, RISING);
  LED_test();
}

float computeDegree(){
  return current_turn / last_rotation;
}

void loop() {
  // Update timer
  current_turn = (float) millis() - turn_start;
  if(last_rotation != 0) drawPicture(computeDegree());
}
