

#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    209
#define BRIGHTNESS  128
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

int id;
int rval;
int gval;
int bval;

#define UPDATES_PER_SECOND 30

void setup() {
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );    
    FastLED.setBrightness(  BRIGHTNESS );
    Serial.begin(1000000);

    initLEDColors();
    FastLED.show();
    Serial.setTimeout(1000);
}

void loop()
{      
  if(Serial.available() > 0){
    char c = (char) Serial.read();
    if(c == 'r') {      
      initLEDColors();
      FastLED.show();
    }
    
    if(c == '@'){      
      Serial.readBytesUntil('#', (char*) leds, NUM_LEDS * 3);  
      FastLED.show();
//      //Serial.print("START");      
//      byte color[4];
//      Serial.readBytesUntil('#', color, 4);
//      int id = color[0];
//      if(id < NUM_LEDS){
//        int rval = color[1];
//        int gval = color[2];
//        int bval = color[3];     
//        leds[id] = CRGB(rval, gval, bval);
//      }
      //Serial.print("END");
    }   
  }
  //FastLED.delay(1000 / UPDATES_PER_SECOND);
}

void initLEDColors() {
  for(int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB::Black;//CRGB( 255, 255, 255);    
  }
}

