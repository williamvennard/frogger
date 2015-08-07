 ---------------------------------------------------------------------

                    BITLIB - BITSCOPE LIBRARY

                     Version 2.0 Build DK06B

             http://www.bitscope.com/software/library/

    Copyright (C) 2013 by BitScope Designs. All Rights Reserved.

 ---------------------------------------------------------------------
 The BITSCOPE LIBRARY (BITLIB) is function call based API for use with
 any model BitScope.  It allows applications to connect to and control
 BitScope without the use of BitScope's Atomic Byte-Code.
 ---------------------------------------------------------------------
 WHAT IS BITSCOPE ?

 BitScope is a mixed signal (analog + digital) data capture device for
 use with a host computer. It is programmable and can be configured as
 a digital  storage oscilloscope,  logic analyzer,  spectrum analyzer,
 data acquisition device, waveform generator or combination of these.
 --------------------------------------------------------------------- 
 WHAT IS ATOMIC BYTE-CODE ?
 
 All BitScopes are built on an abstract virtual machine which executes
 special programs written in as ASCII encoded ABC ("Atomic Byte-Code")
 so operation is script driven. This means any programming language or
 software application  that can  work with ASCII  strings can  be used
 with BitScope. For example, C/C++/Objective, Java/JavaScript, Python,
 Lua, Delphi, MatLab, LabVIEW etc.
 
 ABC is built using a  simple stateless protocol employing an implicit
 handshake which eliminates complex  communication protocols. It means
 different physical interface types, from serial to USB or TCP/IP, can
 all be used the same way.
 --------------------------------------------------------------------- 
 BITSCOPE LIBRARY API
 
 BitScope can be programmed using ABC (via the Link Library, viz).
 
 However, the Bitscope Library  (packaged here) is recommended instead
 because it encapsulates  and generalises ABC programming  via an easy
 to use C function API which makes learning ABC unecessary.
 
 The API offers a set of functions to open a device, send commands and
 receive replies from  a BitScope. The API has been  written in Delphi
 with bindings for C/C++/Objective-C  and Python, but similar bindings
 can be  added for  almost language  that supports  dynamic libraries.
 ---------------------------------------------------------------------
 PROBE FILE (bitscope.prb)

 The probe file defines where the library should look to find BitScope
 devices you have  connected to your PC. Read  the distributed version
 of this file for a complete description of the syntax and semmantics.
 ---------------------------------------------------------------------
                 BitScope Designs. Nov 12, 2013.
 ---------------------------------------------------------------------
