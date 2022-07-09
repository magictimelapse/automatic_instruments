/**
   Serial Xylophone Interface
   Purpose: Interfaces the relais connected to the Arduino's GPIOs and switches them on for <duration>
   @author Michael Rissi
   @email michael.rissi@gmail.com
   @version v1.0.0
*/

#include "SerialCommands.h"

// duration while relais is powered
int duration = 15;

// we have 22 relais connected to the arduino.
const int num_channels = 22;
// translation table from channel to gpio number
const int mch_to_gpio[num_channels][2] = {
  {0, 8},
  {1, 9},
  {2, 10},
  {3, 11},
  {4, 12},
  {5, 13},
  {6, 14},
  {7, 15},
  {8, 16},
  {9, 17},
  {10, 19},
  {11, 18},
  {12, 19},
  {13, 20},
  {14, 21},
  {15, 22},
  {16, 23},
  {17, 25},
  {18, 26},
  {19, 27},
  {20, 28},
  {21, 29}
};
int ch_to_gpio(int channel_nr) {


  // poor man's lookup:
  for (int i = 0; i < num_channels; i++) {
    if (mch_to_gpio[i][0] == channel_nr) {
      return mch_to_gpio[i][1];
    }
  }
  return -1;


}
// Serial Interface //
char serial_command_buffer_[128];
SerialCommands serial_commands_(&Serial, serial_command_buffer_, sizeof(serial_command_buffer_), "\r\n", " ");

//Default handler
void cmd_unrecognized(SerialCommands* sender, const char* cmd) {
  sender->GetSerial()->print("Unrecognized command [");
  sender->GetSerial()->print(cmd);
  sender->GetSerial()->println("]");
}

// Serial command to set the duration of the relais pulse
void cmd_set_duration(SerialCommands *sender) {
  duration = atoi(sender->Next());
  sender->GetSerial()->println(duration);
}

// Serial command to hit the relais for duration in ms.
void cmd_hit_relais(SerialCommands *sender) {
  // multiple relais may be hit at the same time, so we have to scan the string until no more elements appears
  int relais_to_hit[num_channels];
  int relais_counter = 0;

  while (char* arg = sender->Next()) {
    relais_to_hit[relais_counter] = atoi(arg);
    relais_counter++;
  }

  // and hit the relais for duration in ms
  for (int i; i < relais_counter; i++) {
    digitalWrite(ch_to_gpio(relais_to_hit[i]), HIGH);
  }
  delay(duration);
  for (int i; i < relais_counter; i++) {
    digitalWrite(ch_to_gpio(relais_to_hit[i]), LOW);
  }
}


void cmd_instrument(SerialCommands *sender)
{
  sender->GetSerial()->println("xylophone");
}

// define the serial strings identifying the corresponding function
SerialCommand cmd_set_duration_("set_duration", cmd_set_duration);
SerialCommand cmd_hit_relais_("hit_relais", cmd_hit_relais);
SerialCommand cmd_instrument_("instrument", cmd_instrument);


void setup()
{
  Serial.begin(115200);

  for (int i = 0; i < num_channels; i++) {
    pinMode(mch_to_gpio[i][1], OUTPUT);
  }
  
  serial_commands_.SetDefaultHandler(cmd_unrecognized);
  serial_commands_.AddCommand(&cmd_set_duration_);
  serial_commands_.AddCommand(&cmd_hit_relais_);
  serial_commands_.AddCommand(&cmd_instrument_);
  while(!Serial) {};
  Serial.println("ready");

}

void loop()
{
  serial_commands_.ReadSerial();
}

// END FILE
