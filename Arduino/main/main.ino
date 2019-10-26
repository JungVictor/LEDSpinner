#include <FastLED.h>

#define NUM_LEDS      42
#define DATA_PIN      11
#define CLOCK_PIN     13
#define INTERRUPT_PIN 2
#define MAX_DEGREE    180
#define IMAGE_SIZE    31

const int DIFF = (NUM_LEDS - IMAGE_SIZE)/2;
const int EXTRACTION_SIZE = IMAGE_SIZE + IMAGE_SIZE - 1;
const float RAPPORT = EXTRACTION_SIZE / MAX_DEGREE;

unsigned long last_rotation = 0;
unsigned long turn_start;
unsigned long current_turn;

CRGB leds[NUM_LEDS];
CRGB picture[EXTRACTION_SIZE][IMAGE_SIZE];

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
  for(int i = 0; i < NUM_LEDS; i++) leds[i] = CRGB::White;
  FastLED.show();
  delay(30);
  for(int i = 0; i < NUM_LEDS; i++) leds[i] = CRGB::Black;
  FastLED.show();
}

void drawPicture(int degree){
  int index = int(degree * RAPPORT);
  if(degree < MAX_DEGREE) for(int i = DIFF; i < DIFF+IMAGE_SIZE; i++) leds[i] = picture[index][i];
  else for(int i = DIFF+IMAGE_SIZE-1; i > DIFF; i--) leds[i] = picture[index][i];
  FastLED.show();
}

void oneTurn(){
  last_rotation = current_turn;
  current_turn = 0;
  turn_start = millis();
  drawPicture(0);  
}

void setup() {
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, GBR>(leds, NUM_LEDS);
  FastLED.setBrightness(5);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), oneTurn, RISING);
  LED_test();
}

int computeDegree(){
  return (int(last_rotation / current_turn) * 360);
}

void loop() {
  // Update timer
  current_turn = millis() - turn_start;
  if(last_rotation != 0) drawPicture(computeDegree());
}
