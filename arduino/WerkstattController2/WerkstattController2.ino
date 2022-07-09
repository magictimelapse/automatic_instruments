/*
   Stepper test for Seeed Motor Shield V2
   loovee @ 15 Mar, 2016
*/


#include "SerialCommands.h"
#define VCOEPIN 6
#define VCAPIN 3
#define GATEPIN 7 
#define CLICKPIN 8
unsigned int attack = 50;
unsigned int sustain = 2000;
unsigned int release = 50;
int vca = 0;
int startNoteMillis = 0;
//#define DEBUG 

// Serial Interface
char serial_command_buffer_[64];
SerialCommands serial_commands_(&Serial, serial_command_buffer_, sizeof(serial_command_buffer_), "\r\n", " ");

//This is the default handler, and gets called when no other command matches.
void cmd_unrecognized(SerialCommands* sender, const char* cmd)
{
  #if defined(DEBUG)
  sender->GetSerial()->print("Unrecognized command [");
  sender->GetSerial()->print(cmd);
  sender->GetSerial()->println("]");
  #endif
}

void cmd_click(SerialCommands *sender)
{
  digitalWrite(CLICKPIN,HIGH);
  delay(10);
  digitalWrite(CLICKPIN,LOW);
  #if defined(DEBUG)
  sender->GetSerial()->println("click");
  #endif
  
}

void cmd_set_adsr(SerialCommands *sender)
{
  attack = (int)(atof(sender->Next())*1000);
  sustain =(int)(atof(sender->Next())*1000);
  release = (int)(atof(sender->Next())*1000);
  #if defined(DEBUG)
  sender->GetSerial()->print(attack);
  sender->GetSerial()->print(" ");
  sender->GetSerial()->print(sustain);
  sender->GetSerial()->print(" ");
  sender->GetSerial()->println(release);
  #endif

}

void cmd_set_vcoe(SerialCommands *sender)
{
  int vcoe = atoi(sender->Next());
  analogWrite(VCOEPIN, vcoe);
  digitalWrite(GATEPIN,true);
  #if defined(DEBUG)
  sender->GetSerial()->println(vcoe);
  #endif
  startNoteMillis = millis();
}

void cmd_set_vca(SerialCommands *sender)
{
  vca = atoi(sender->Next());
  if(vca == 0)
  {
    digitalWrite(GATEPIN,false);
  }
  //analogWrite(VCAPIN, vca);
  #if defined(DEBUG)
  sender->GetSerial()->println(vca);
  #endif
}

void cmd_instrument(SerialCommands *sender)
{
  #if defined(DEBUG)
  sender->GetSerial()->println("synth");
  #endif
}

SerialCommand cmd_set_vcoe_("vcoe", cmd_set_vcoe);
SerialCommand cmd_set_vca_("vca", cmd_set_vca);
SerialCommand cmd_set_adsr_("adsr", cmd_set_adsr);
SerialCommand cmd_click_("click",cmd_click);

int play_ADSR()
{
  unsigned int currentMillis = millis();
  unsigned int delta = currentMillis - startNoteMillis;
  //Serial.print("delta: ");
  //Serial.println(delta);
  int vca_to_play;
  if (delta < attack)
  {
    
    vca_to_play = (int)(1.0*delta / attack * vca);

  }
  else if (delta < attack + sustain)
  {
   
    vca_to_play = vca;
  }
  else if (delta < attack + sustain + release)
  {
    
    vca_to_play = (int)(1.0*vca - (1.0*delta - attack - sustain) / release * vca);

  }
  else
  {
   vca_to_play = 0;
   digitalWrite(GATEPIN,false);
  }
  analogWrite(VCAPIN, vca_to_play);
}


void setup()
{
  Serial.begin(115200);
  

  pinMode(VCOEPIN, OUTPUT);
  pinMode(VCAPIN, OUTPUT);
  pinMode(GATEPIN, OUTPUT);
  pinMode(CLICKPIN, OUTPUT);
  serial_commands_.SetDefaultHandler(cmd_unrecognized);
  serial_commands_.AddCommand(&cmd_set_vcoe_);
  serial_commands_.AddCommand(&cmd_set_vca_);
  serial_commands_.AddCommand(&cmd_set_adsr_);
  serial_commands_.AddCommand(&cmd_click_);
  digitalWrite(GATEPIN,false);
  digitalWrite(CLICKPIN,false);

  Serial.println("ready");

}

void loop()
{
 serial_commands_.ReadSerial();

  play_ADSR();
  //delay(100);
  //Serial.println("fsdf");






}

// END FILE
