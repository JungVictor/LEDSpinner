#include <FastLED.h>
#include "image.h"
#define DATA_PIN      10
#define CLOCK_PIN     13
#define INTERRUPT_PIN 2

const boolean UPDATE_IMAGE = IMAGE_TIME > 0;

float last_rotation = 0;
float turn_start;
float current_turn;
float last_image_time = 0;

CRGB leds[NUM_LEDS];
int IMAGE = 0;

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
  FastLED.show();
}

int getSize(int led){
  return POSITIONS[led+1] - POSITIONS[led];
}

int getIndex(float degree, int led){
  return round(degree * (getSize(led) - 1)) + POSITIONS[led];
}

CRGB getColor(float degree, int led, int image){
  return COLORS[PIXELS[image][getIndex(degree, led)]];
}

// degree = 1 => 360°
void drawPicture(float degree){
  if(degree > 1) degree = 1;
  // 180 <= degree < 360
  if(degree > 0.5){
    degree -= 0.5;
    degree *= 2;
    for(int i = 0; i < NUM_LEDS; i++) leds[i] = getColor(degree, NUM_LEDS - 1 - i, IMAGE);
  }
  // 0 <= degree < 180
  else {
    degree *= 2;
    for(int i = 0; i < NUM_LEDS; i++) leds[i] = getColor(degree, i, IMAGE);
  }
  
  FastLED.show();
}

void oneTurn(){
  turn_start = (float) millis();
  last_rotation = current_turn;
  current_turn = 0;
}

float computeDegree(){
  return current_turn / last_rotation;
}

void draw(){
  drawPicture(computeDegree());
}

void setup() {
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, BGR>(leds, NUM_LEDS);
  FastLED.setBrightness(3);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), oneTurn, RISING);
  LED_test();
}

void updateTimers(){
  current_turn = (float) millis() - turn_start;
}

void updateImage(){
  if(!UPDATE_IMAGE) return;
  float t = (float) millis();
  if(t - last_image_time >= IMAGE_TIME){
    IMAGE++;
    if(IMAGE >= N_IMAGES) IMAGE = 0;
    last_image_time = t;
  }
}

void loop() {
  updateTimers();
  updateImage();
  draw();
}
