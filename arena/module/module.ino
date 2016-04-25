#include <Servo.h>

#define outA 10
#define outB 11

class Activator {
  public:
    Activator(int pin);
    Activator(int pin, bool continuous);
    bool active();
    void activate();

  private:
    int pinNo;
    bool cont;
    bool isActive;    
};

Activator A(5);
Activator B(6, true);
Activator list[] = {A, B};
Servo servo;

bool triggered = false;

void setup() {
  servo.attach(outA);

}

void loop() {
  if(checkActivators()) {
    if(!triggered) {
      triggerModule();
      triggered = true;
    }
  } else {
    if(triggered) {
      revertModule();
      triggered = false;
    }
  }
  attemptActivation();
  delay(50);

}

/**
 * Activates the module in whatever way it's supposed to.
 */
void triggerModule() {
  servo.write(90);
}

/**
 * Attempts to deactivate the module.
 */
void revertModule() {
  servo.write(0);
}

/**
 * Returns true iff all activators are active.
 */
bool checkActivators() {
  bool results = true;
  for(int i = 0; i < sizeof(list) / sizeof(*list); i++) {
    list[i].activate();
    results &= list[i].active();
  }
  return results;
}

/**
 * Attempts to set active status on all activators.
 */
void attemptActivation() {
  for(int i = 0; i < sizeof(list) / sizeof(*list); i++) {
    list[i].activate();
  }
}


/*
 * Definitions of Activator below
 */


Activator::Activator(int pin) {
  pinNo = pin;
  cont = false;
  isActive = false;
  pinMode(pinNo, INPUT_PULLUP);
}

Activator::Activator(int pin, bool continuous) {
  pinNo = pin;
  cont = continuous;
  isActive = false;
  pinMode(pinNo, INPUT_PULLUP);
}

/**
 * Call this regularly to detect activations.
 */
void Activator::activate() {
  if(digitalRead(pinNo) == LOW) {
    isActive = true;
  }
}

/**
 * Returns whether this is active or not.
 */
bool Activator::active() {
  if(cont) {
    if(digitalRead(pinNo) == LOW) {
      return true;
    } else {
      return false;
    }
  } else {
    return isActive;
  }
}


