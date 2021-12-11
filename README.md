# Virtual Machine

This virtual machine was built for my Principles of Computer Science class. It is a 16-bit machine that performs the low-level operations that would be taking place at the circuitry level. The machine can either read in a custom Assembly language (files that end in .asl) or the equivalent binary code for it (files that end in .eoc).

Commands:

| Command                 | Action                                                                                                                                |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| load (filename).eoc     | Loads a .eoc file into memory                                                                                                         |
| assemble (filename).asl | Loads a .asl file into memory                                                                                                         |
| run                     | Runs loaded file                                                                                                                      |
| dump                    | Displays the page of memory that the Instruction Pointer is on.                                                                       |
| registers               | Displays the contents of the general purpose registers.                                                                               |
| state                   | Displays output of 'dump' and 'registers' as well as the contents of the NZP Register, Instruction Pointer, and Instruction Register. |

Included are several different test files, both .eoc and .asl, that showcase the machine in action.
