	.ORIG	x1000
; R5,R6 = R1/R0
; R5 is quotient
; R6 is remainder
; Alters R0, R1
DIV	LD	R1 NUM1
	LD	R5 QUOT
	ST	R1 REMAIN
LOOP	LD	R0 NUM2
	LD	R1 REMAIN
	BR	NZ END
	JSR	SUB
	ST	R6 REMAIN
	ADD	R5 #1
	JMP	LOOP
END	PUT	R5
	LD	R4 NEWL
	PUTC	R4
	PUT	R6
	HALT
NUM1	.SET	30
NUM2	.SET	6
QUOT	.SET	0
REMAIN	.SET	0
; R6 = R1 - R0
;R0 is altered
SUB	NOT	R0 R0
	ADD	R0 #1
	ADD	R6 R1 R0
	RET
NEWL	.ASCII	R
	.END