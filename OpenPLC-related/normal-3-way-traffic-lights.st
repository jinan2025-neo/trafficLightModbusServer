PROGRAM program0
  VAR
    Run_AM AT %QX100.1 : BOOL := true;
    N_red AT %QX0.0 : BOOL := false;
    N_amber AT %QX0.1 : BOOL := false;
    N_green AT %QX0.2 : BOOL := false;
    EW_red AT %QX0.3 : BOOL := false;
    EW_amber AT %QX0.4 : BOOL := false;
    EW_green AT %QX0.5 : BOOL := false;
    S_red AT %QX0.6 : BOOL := false;
    S_amber AT %QX0.7 : BOOL := false;
    S_green AT %QX1.0 : BOOL := false;
  END_VAR
  VAR
    T0_Q : BOOL := false;
    T1_Q : BOOL := false;
    T2_Q : BOOL := false;
    T3_Q : BOOL := false;
    reset_counter : BOOL := false;
    State_0 : BOOL;
    State_1 : BOOL;
    State_2 : BOOL;
    State_3 : BOOL;
    State_4 : BOOL;
    State_5 : BOOL;
    State_6 : BOOL;
    State_7 : BOOL;
    State_8 : BOOL;
    State_9 : BOOL;
    State_10 : BOOL;
    State_11 : BOOL;
    TP1 : TP;
    TP2 : TP;
    TP3 : TP;
    TP4 : TP;
    TP5 : TP;
    TP6 : TP;
    TP7 : TP;
    TP8 : TP;
    TP9 : TP;
    TP10 : TP;
    TP11 : TP;
    TP12 : TP;
  END_VAR
  VAR
    mode_flag AT %QX100.0 : BOOL := false;
  END_VAR
  VAR
    green_time : TIME;
    IN0 : TIME := T#4s;
    IN1 : TIME := T#8s;
    _TMP_MOVE259_ENO : BOOL;
    _TMP_MOVE259_OUT : TIME;
    _TMP_MOVE131_ENO : BOOL;
    _TMP_MOVE131_OUT : TIME;
  END_VAR

  Run_AM := Run_AM;
  TP1(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND Run_AM OR NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#2s);
  State_0 := TP1.Q;
  TP2(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_0) AND Run_AM, PT := T#3s);
  State_1 := TP2.Q;
  TP3(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := green_time);
  State_2 := TP3.Q;
  TP4(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#3s);
  State_3 := TP4.Q;
  TP5(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_3) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#2s);
  State_4 := TP5.Q;
  TP6(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#3s);
  State_5 := TP6.Q;
  TP7(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := green_time);
  State_6 := TP7.Q;
  TP8(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#3s);
  State_7 := TP8.Q;
  TP9(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_9) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#2s);
  State_8 := TP9.Q;
  TP10(IN := NOT(State_11) AND NOT(State_10) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#3s);
  State_9 := TP10.Q;
  TP11(IN := NOT(State_11) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := green_time);
  State_10 := TP11.Q;
  TP12(IN := NOT(State_10) AND NOT(State_9) AND NOT(State_8) AND NOT(State_7) AND NOT(State_6) AND NOT(State_5) AND NOT(State_4) AND (NOT(State_3) OR NOT(State_3)) AND NOT(State_2) AND NOT(State_1) AND NOT(State_0) AND Run_AM, PT := T#3s);
  State_11 := TP12.Q;
  EW_red := State_0 OR State_1 OR State_10 OR State_11 OR State_2 OR State_3 OR State_4 OR State_5 OR State_8 OR State_9;
  N_red := State_0 OR State_1 OR State_10 OR State_11 OR State_4 OR State_5 OR State_6 OR State_7 OR State_8 OR State_9;
  S_red := State_0 OR State_1 OR State_2 OR State_3 OR State_4 OR State_5 OR State_6 OR State_7 OR State_8 OR State_9;
  N_amber := State_1 OR State_3;
  N_green := State_2;
  EW_amber := State_5 OR State_7;
  EW_green := State_6;
  S_amber := State_11 OR State_9;
  S_green := State_10;
  _TMP_MOVE259_OUT := MOVE(EN := mode_flag, IN := IN0, ENO => _TMP_MOVE259_ENO);
  IF _TMP_MOVE259_ENO THEN
      green_time := _TMP_MOVE259_OUT;
  END_IF;
  _TMP_MOVE131_OUT := MOVE(EN := NOT(mode_flag), IN := IN1, ENO => _TMP_MOVE131_ENO);
  IF _TMP_MOVE131_ENO THEN
      green_time := _TMP_MOVE131_OUT;
  END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#200ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION

(*DBG:char md5[] = "d0baaf7fd8272d1f74d8e6524d72354d";*)
(*DBG:/**)
(*DBG: * This file is part of OpenPLC Runtime*)
(*DBG: **)
(*DBG: * Copyright (C) 2023 Autonomy, GP Orcullo*)
(*DBG: * Based on the work by GP Orcullo on Beremiz for uC*)
(*DBG: **)
(*DBG: * This program is free software; you can redistribute it and/or*)
(*DBG: * modify it under the terms of the GNU General Public License*)
(*DBG: * as published by the Free Software Foundation; either version 2*)
(*DBG: * of the License, or (at your option) any later version.*)
(*DBG: **)
(*DBG: * This program is distributed in the hope that it will be useful,*)
(*DBG: * but WITHOUT ANY WARRANTY; without even the implied warranty of*)
(*DBG: * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the*)
(*DBG: * GNU General Public License for more details.*)
(*DBG: **)
(*DBG: * You should have received a copy of the GNU General Public License*)
(*DBG: * along with this program; If not, see <http://www.gnu.org/licenses/>.*)
(*DBG: **)
(*DBG: */*)
(*DBG:*)
(*DBG:#include <stdbool.h>*)
(*DBG:*)
(*DBG:#include "iec_types_all.h"*)
(*DBG:#include "POUS.h"*)
(*DBG:*)
(*DBG:#define SAME_ENDIANNESS      0*)
(*DBG:#define REVERSE_ENDIANNESS   1*)
(*DBG:*)
(*DBG:uint8_t endianness;*)
(*DBG:*)
(*DBG:*)
(*DBG:extern PROGRAM0 RES0__INSTANCE0;*)
(*DBG:*)
(*DBG:static const struct {*)
(*DBG:    void *ptr;*)
(*DBG:    __IEC_types_enum type;*)
(*DBG:} debug_vars[] = {*)
(*DBG:    {&(RES0__INSTANCE0.RUN_AM), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.N_RED), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.N_AMBER), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.N_GREEN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.EW_RED), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.EW_AMBER), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.EW_GREEN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.S_RED), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.S_AMBER), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.S_GREEN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.T0_Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.T1_Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.T2_Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.T3_Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.RESET_COUNTER), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_0), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_1), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_2), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_3), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_4), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_5), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_6), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_7), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_8), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_9), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_10), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.STATE_11), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP1.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP2.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP3.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP4.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP5.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP6.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP7.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP8.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP9.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP10.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP11.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.EN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.PT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.Q), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.ET), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.STATE), SINT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.PREV_IN), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.CURRENT_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.TP12.START_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.MODE_FLAG), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.GREEN_TIME), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.IN0), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.IN1), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE259_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE259_OUT), TIME_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE131_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE131_OUT), TIME_ENUM},*)
(*DBG:};*)
(*DBG:*)
(*DBG:#define VAR_COUNT               155*)
(*DBG:*)
(*DBG:uint16_t get_var_count(void)*)
(*DBG:{*)
(*DBG:    return VAR_COUNT;*)
(*DBG:}*)
(*DBG:*)
(*DBG:size_t get_var_size(size_t idx)*)
(*DBG:{*)
(*DBG:    if (idx >= VAR_COUNT)*)
(*DBG:    {*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:    switch (debug_vars[idx].type) {*)
(*DBG:    case TIME_ENUM:*)
(*DBG:        return sizeof(TIME);*)
(*DBG:    case SINT_ENUM:*)
(*DBG:        return sizeof(SINT);*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return sizeof(BOOL);*)
(*DBG:    default:*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void *get_var_addr(size_t idx)*)
(*DBG:{*)
(*DBG:    void *ptr = debug_vars[idx].ptr;*)
(*DBG:*)
(*DBG:    switch (debug_vars[idx].type) {*)
(*DBG:    case TIME_ENUM:*)
(*DBG:        return (void *)&((__IEC_TIME_t *) ptr)->value;*)
(*DBG:    case SINT_ENUM:*)
(*DBG:        return (void *)&((__IEC_SINT_t *) ptr)->value;*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return (void *)&((__IEC_BOOL_t *) ptr)->value;*)
(*DBG:    default:*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void force_var(size_t idx, bool forced, void *val)*)
(*DBG:{*)
(*DBG:    void *ptr = debug_vars[idx].ptr;*)
(*DBG:*)
(*DBG:    if (forced) {*)
(*DBG:        size_t var_size = get_var_size(idx);*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case TIME_ENUM: {*)
(*DBG:            memcpy(&((__IEC_TIME_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_TIME_t *) ptr)->value = *((TIME *) val);*)
(*DBG:            ((__IEC_TIME_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case SINT_ENUM: {*)
(*DBG:            memcpy(&((__IEC_SINT_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_SINT_t *) ptr)->value = *((SINT *) val);*)
(*DBG:            ((__IEC_SINT_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case BOOL_ENUM: {*)
(*DBG:            memcpy(&((__IEC_BOOL_t *) ptr)->value, val, var_size);*)
(*DBG:            //((__IEC_BOOL_t *) ptr)->value = *((BOOL *) val);*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    } else {*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case TIME_ENUM:*)
(*DBG:            ((__IEC_TIME_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case SINT_ENUM:*)
(*DBG:            ((__IEC_SINT_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case BOOL_ENUM:*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void swap_bytes(void *ptr, size_t size) *)
(*DBG:{*)
(*DBG:    uint8_t *bytePtr = (uint8_t *)ptr;*)
(*DBG:    size_t i;*)
(*DBG:    for (i = 0; i < size / 2; ++i) *)
(*DBG:    {*)
(*DBG:        uint8_t temp = bytePtr[i];*)
(*DBG:        bytePtr[i] = bytePtr[size - 1 - i];*)
(*DBG:        bytePtr[size - 1 - i] = temp;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void trace_reset(void)*)
(*DBG:{*)
(*DBG:    for (size_t i=0; i < VAR_COUNT; i++) *)
(*DBG:    {*)
(*DBG:        force_var(i, false, 0);*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void set_trace(size_t idx, bool forced, void *val)*)
(*DBG:{*)
(*DBG:    if (idx >= 0 && idx < VAR_COUNT) *)
(*DBG:    {*)
(*DBG:        if (endianness == REVERSE_ENDIANNESS)*)
(*DBG:        {*)
(*DBG:            // Aaaaarghhhh... Stupid AVR is Big Endian.*)
(*DBG:            swap_bytes(val, get_var_size(idx));*)
(*DBG:        }*)
(*DBG:*)
(*DBG:        force_var(idx, forced, val);*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void set_endianness(uint8_t value)*)
(*DBG:{*)
(*DBG:    if (value == SAME_ENDIANNESS || value == REVERSE_ENDIANNESS)*)
(*DBG:    {*)
(*DBG:        endianness = value;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)