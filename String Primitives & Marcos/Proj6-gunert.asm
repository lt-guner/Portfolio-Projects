TITLE Proj6_gunert     (Pro6_guner.asm)

; Author: 
; Last Modified: 2021-05-27
; OSU email address: gunert@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: Project 6                Due Date: 2021-06-06
; Description: This program asks the user for 10 different string inputs that
;			   are numbers. It converts each string into a number and stores them
;			   on an SWDORD array. From there, it totals those numbers and finds the 
;			   average, and then converts them to strings. Finally, it converts
;			   the entire SDWORD array into a string and prints the array,
;			   sum, and average using writestring.

INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Gets the user input and also displays the error message if the user does not 
; enter a valid number. If the number is invalid they are asked for another input
;
; Preconditions:
;	stringInput, stringError, stringTryAgain, and userInputString are declared BYTE strings
;	sLen and choice are DWORDs
;
; Postconditions: All registers are preserved, so no changes
;
; Receives: 
;	stringInput = askForInput ([EBP+20])
;	stringError = errotInput ([EBP+16])
;	stringTryAgain = tryAgain ([EBP+12])
;	sLen = stringLength
;	userInputString = userInput ([EBP+8])
;	choice = choiceLoad
;
; Returns: userInputString contains a string input from the user and sLen contains the length of input
; ---------------------------------------------------------------------------------
mGetString MACRO	stringInput, stringError, stringTryAgain, sLen, userInputString, choice
	
	; local sgements for mGstring
	LOCAL	_checkError, _endGetString

	; push used registers to the stack
	PUSH	EDX
	PUSH	ECX
	PUSH	EAX
	
; --------------------------
; CMP choice to 1 to determine if this is the first attempt to enter valid number.
; If it is the first attempt, display stringInput and get userInputString.
; Store EAX into sLen.
; --------------------------
	CMP		choice, 1
	JNE		_checkError
	MOV		EDX, stringInput
	CALL	WriteString
	MOV		ECX, MAXLENGTHINPUT
	MOV		EDX, userInputString
	CALL	ReadString
	MOV		sLen, EAX
	JMP		_endGetString

; --------------------------
; CMP choice to 2 to determine if the user previously entered a wrong number.
; If they have, display stringError then ask for input by displaying stringTryAgain.
; Get the userInputString and save EAX to sLen
; --------------------------
_checkError:
	CMP		choice, 2
	JNE		_endGetString
	MOV		EDX, stringError
	CALL	WriteString
	MOV		EDX, stringTryAgain
	CALL	WriteString
	MOV		ECX, MAXLENGTHINPUT
	MOV		EDX, userInputString
	CALL	ReadString
	MOV		sLen, EAX

; macro ends and registers on stack are popped	
_endGetString:
	POP		EAX
	POP		ECX
	POP		EDX	
ENDM

; ---------------------------------------------------------------------------------
; Name: mDisplatString
;
; Display the list of inputs, the sum, and the average as a string
;
; Preconditions:
;	outputListStr, outputSumStr, and outputAvgStr are declated BYTE strings
;	numListString, sumString, sumString store the necessary numbers as strings
;
; Postconditions: EDX is preserved, so no changes
;
; Receives: 
;	stringList = numListString [EBP+20]
;	stringSum = sumString [EBP+12]
;	stringAvg = avgString [EBP+16]
;	listOutputString = outputListStr [EBP+24]
;	sumOutputString = outputSumStr [EBP+28]
;	avgOutputstring = outputAvgStr [EBP+32]
;
; Returns: nothing
; ---------------------------------------------------------------------------------
mDisplayString MACRO stringList, stringSum, stringAvg, listOutputString, sumOutputString, avgOutputstring
	
	;push EDX to stack to preserve the variables
	PUSH	EDX

	;display the list of user inputs
	CALL	CrLf
	MOV		EDX, listOutputString
	CALL	WriteString
	MOV		EDX, stringList
	CALL	WriteString
	CALL	CrLf

	;display the sum
	MOV		EDX, sumOutputString
	CALL	WriteString
	MOV		EDX, stringSum
	CALL	WriteString
	CALL	CrLf

	;display the average
	MOV		EDX, avgOutputstring
	CALL	WriteString
	MOV		EDX, stringAvg
	CALL	WriteString
	CALL	CrLf

	;pop EDX to restore value
	POP		EDX
ENDM

;constants
ARRAYSIZE = 10
MAXLENGTHINPUT	= 13

.data
;display strings
askForInput		BYTE		"Please enter an signed number: ",0
errorInput		BYTE		"ERROR: You did not enter a signed number or your number was too big / too small.",13,10,0
tryAgain		BYTE		"Please try again: ",0
outputListStr	BYTE		"You entered the following numbers:",13,10,0
outputAvgStr	BYTE		"The rounded average is: ",0
outputSumStr	BYTE		"The sum of these numbers is: ",0

;all variables used for storing data
userInput		BYTE		MAXLENGTHINPUT DUP(?)							;a string input from the user
userArray		SDWORD		ARRAYSIZE DUP(?)								;array of inputs from the user
arrayCounter	DWORD		0												;arrayCounter is used to increment each slot of 4 bytes in userArray
sumString		BYTE		MAXLENGTHINPUT DUP(?)							;stores the sum of userArray into a string
avgString		BYTE		MAXLENGTHINPUT DUP(?)							;stores the average of userArray into a string
numListString	BYTE		200	DUP(?)										;a huge string to store all values in userArray into a giant string list

;headings and intros
headingOne		BYTE		"PROGRAMMING ASSIGNMENT 6: Designing low-level I/O procedures",13,10,0
headingTwo		BYTE		"Written by: Timur Guner",13,10,13,10,0
introOne		BYTE		"Please provide 10 signed decimal integers.",13,10,0
introTwo		BYTE		"Each number needs to be small enough to fit inside a 32 bit register. After you have finished inputting the raw numbers",13,10
				BYTE		"I will display a list of the integers, their sum, and their average value (floor / round down).",13,10,13,10,0

.code
main PROC
	
	;push introduction parameters to the stack and call introduction
	PUSH	OFFSET introTwo
	PUSH	OFFSET introOne
	PUSH	OFFSET headingTwo
	PUSH	OFFSET headingOne
	CALL	introduction

	;counter used to loop through to get ARRAYSIZE inputs
	MOV		ECX, ARRAYSIZE
_readLoop:
	;push ReadVal parameters to the stack and call ReadVal
	PUSH	arrayCounter
	PUSH	OFFSET userArray
	PUSH	OFFSET askForInput
	PUSH	OFFSET errorInput
	PUSH	OFFSET tryAgain
	PUSH	OFFSET userInput
	CALL	ReadVal							;{parameters: arrayCounter (value, input), userArray (reference, input), askForInput (reference, input), errorInput (reference, input), tryAgain (reference, input), userInput (reference, input))
	ADD		arrayCounter, 4					;increase arrayCounter add change address of userArray in ReadVal
	LOOP	_readLoop						;loop readLoop to get a new value into the userArray. When ECX is 0, escape the LOOP

	;push WriteVal parameters to the stack and call WriteVal
	PUSH	OFFSET outputAvgStr
	PUSH	OFFSET outputSumStr
	PUSH	OFFSET outputListStr
	PUSH	OFFSET numListString
	PUSH	OFFSET avgString
	PUSH	OFFSET sumString
	PUSH	OFFSET userArray
	CALL	WriteVal

	Invoke ExitProcess,0					; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: introduction
;
; Displays introductions and intrsuctions to the user
;
; Preconditions: 
;	headingOne, headingTwo, intro1, and intro2 are declared strings
;
; Postconditions: None because all registers are preserved by pushing and popping from the stack
;
; Receives: 
;	headingOne [EBP+12]
;	headingTwo [EBP+16]
;	introOne [EBP+20]
;	introTwo [EBP+24]
;
; Returns: nothing
; ---------------------------------------------------------------------------------
introduction PROC
	
	;pushed used registers to the stack
	PUSH	EDX
	PUSH	EBP
	MOV		EBP, ESP

	;dispay headingOne
	MOV		EDX, [EBP+12]
	CALL	WriteString

	;display headingTwo
	MOV		EDX, [EBP+16]
	CALL	WriteString

	;display introOne
	MOV		EDX, [EBP+20]
	CALL	WriteString

	;display introTwo
	MOV		EDX, [EBP+24]
	CALL	WriteString

	;pop used regisers and and ret stack to starting position
	POP		EBP
	POP		EDX
	RET		16

introduction ENDP

; ---------------------------------------------------------------------------------
; Name: ReadVal
;
; The procedure takes a string input from the user and turns it into an SDWORD.
; If the conversion results is a number too big or too small, then the user is 
; prompted again to a valid input until they enter a valid input. The converted
; value is then stored in an SDWORD array.
;
; Preconditions: 
;	arrayCounter is a declared DWORD
;	userInput is a declated SDWORD array
;	userArray, askForInput, errorInput, and tryAgain are strings
;
; Postconditions: None because all registers are preserved by pushing and popping from the stack
;
; Receives: 
;	userInput [EBP+8]
;	tryAgain [EBP+12]
;	errorInput [EBP+16]
;	askForInput [EBP+20]
;	userArray [EBP+24]
;	arrayCounter [EBP+28]
;
; Returns:
;	userInput is populated with a new user input string
;	userArray has signedVal appended to a new slot
; ---------------------------------------------------------------------------------
ReadVal PROC

	LOCAL	stringLength:DWORD				;Length of string input from user
	LOCAL	previousVal:SDWORD				;holds the total of the previous converted string characters in the conversion cycle
	LOCAL	signedVal:SDWORD				;final value after conversion
	LOCAL	choiceLoad:DWORD				;used to determine which strings to load in mGetString

	; push all registers used during procedure
	PUSH	EAX
	PUSH	EBX
	PUSH	ECX
	PUSH	EDX
	PUSH	EDI
	PUSH	ESI

; --------------------------
; getInput is the first attempt to get a valid input in this procedure call.
; choiceLload and previousVal are set to 1 and 0. choiceLoad determines what
; strings to load and write in mGetString. mGetString is passed askForInput, 
; errorInput, tryAgain, stringLength, userInput, and choiceLead. The read string
; is storre in userInput [EBP+8]
; --------------------------
_getInput:
	MOV		choiceLoad,	1
	MOV		previousVal, 0
	mGetString	[EBP+20], [EBP+16], [EBP+12], stringLength, [EBP+8], choiceLoad
	MOV		ESI, [EBP+8]

; The first thing to check is if sting began with a sign and then continue onto the next position
_checkSign:
	LODSB	
	CMP		AL, 45
	JE		_negativeNextStep				;if the value is negative jump to _negativeNextStep to start at the next position
	CMP		AL, 43
	JE		_positiveNextStep				;if the value is positive jump to _positiveNextStep to start at the next position

; if the value did not begin with a + or - sign we assume its postive and reset ESI to beginning of userInput
_positiveBytes:
	MOV		ESI, [EBP+8]

; --------------------------
; _positiveBytesLoop begins the procress of parsing a positive string into an SDWORD.
; It first compares the ASCII input to make sure it is in the range of 48 - 57. If it is
; subract 48 from AL to get the actual digit. If not in range go to _errorError to get a new input.
; Next steps involve the conversion of a the string into SWORD by using the formula
; 10 * numInt + (numChar - 48), where numInt are the total of the digits converted so far and numChar is
; the current BYTE of the input string. Once complete, _postiveBytesLoop is looped until stringLength
; is zero.
; --------------------------
_postiveBytesLoop:
	MOV		EAX, 0
	LODSB									;load the current BYTE into AL
	CMP		AL, 48
	JB		_errorError						;compare the loaded byte to see if it is greater than or equal to 48 which is 0 in ASCII. If not jump to _errorError
	CMP		AL, 57
	JA		_errorError						;compare the loaded byte to see if it is less than or equal to 57 which is 9 in ASCII. If not jump to _errorError
	SUB		AL, 48							;sub 48 from AL to to get the actual decimal value
	
	MOV		EDX, 10	
	MOV		EBX, EAX
	MOV		EAX, previousVal
	JO		_errorError						;code above assigned 10 to EDX, the current value of EAX into EBX, and then the current convert digits so far (previousVal) in EAX. If overflow was triggered, jump to _errorError
	IMUL	EDX
	JO		_errorError						;multiply EAX by EDX and it overflow flag was triggered, jump to _errorError
	ADD		EAX, EBX
	JO		_errorError						;Add the current value of EBX to EAX and jump to _errorError if overflow flag was triggered
	MOV		signedVal, EAX			
	MOV		previousVal, EAX				;assign the conversion to the local variables

;decrement stringLength by 1 and if it reaches zero, jump out of loop and go _endReadVal
_positiveNextStep:
	DEC		stringLength
	CMP		stringLength, 0
	JA		_postiveBytesLoop

	JMP		_endReadVal

; --------------------------
; _negativeBytesLoop begins the procress of parsing a legative string into an SDWORD.
; It first compares the ASCII input to make sure it is in the range of 48 - 57. If it is
; subract 48 from AL to get the actual digit. If not in range go to _errorError to get a new input.
; Next steps involve the conversion of a the string into SWORD by using the formula
; 10 * numInt + (numChar - 48), where numInt are the total of the digits converted so far and numChar is
; the current BYTE of the input string. Once complete, _negativeBytesLoop is looped until stringLength
; is zero.
; --------------------------
_negativeBytesLoop:
	MOV		EAX, 0					
	LODSB									;load the current BYTE into AL
	CMP		AL, 48
	JB		_errorError						;compare the loaded byte to see if it is greater than or equal to 48 which is 0 in ASCII. If not jump to _errorError
	CMP		AL, 57
	JA		_errorError						;compare the loaded byte to see if it is less than or equal to 57 which is 9 in ASCII. If not jump to _errorError
	SUB		AL, 48							;sub 48 from AL to to get the actual decimal value
	
	MOV		EDX, 10
	MOV		EBX, EAX
	NEG		EBX								;since this a negative input we need to negate the postive integers
	MOV		EAX, previousVal
	JO		_errorError						;code above assigned 10 to EDX, the current value of EAX into EBX, and then the current convert digits so far (previousVal) in EAX. If overflow was triggered, jump to _errorError
	IMUL	EDX
	JO		_errorError						;multiply EAX by EDX and it overflow flag was triggered, jump to _errorError
	ADD		EAX, EBX
	JO		_errorError						;Add the current value of EBX to EAX and jump to _errorError if overflow flag was triggered
	MOV		signedVal, EAX
	MOV		previousVal, EAX				;assign the conversion to the local variables

;decrement stringLength by 1 and if it reaches zero, jump out of loop and go _endReadVal	
_negativeNextStep:
	DEC		stringLength
	CMP		stringLength, 0
	JA		_negativeBytesLoop

	JMP		_endReadVal

; --------------------------
; _errorError is the next attempr to get a valid input in this procedure call, 
; if the user entered an invalid number. choiceLload is set to 2 so we know to process
; the error messages and input in mGetString. mGetString is passed askForInput, 
; errorInput, tryAgain, stringLength, userInput, and choiceLead. The read string
; is storre in userInput [EBP+8] and sLen in stringLength. Once complete, reset choiceLoad
; to 1 and previousVal to 0, then jump back to _checksign
;---------------------------
_errorError:
	MOV		choiceLoad, 2
	mGetString	[EBP+20], [EBP+16], [EBP+12], stringLength, [EBP+8], choiceLoad
	MOV		ESI, [EBP+8]
	MOV		choiceLoad,	1
	MOV		previousVal, 0
	JMP		_checkSign

; these are the the final steps of ReadVal
_endReadVal:
	
	; store the new value of signeVal into the the next slot of userArray
	MOV		EDI, [EBP+24]			
	ADD		EDI, [EBP+28]					;load the address of userArrary into EDI and add the current index to EDI
	MOV		EAX, signedVal
	MOV		[EDI], EAX						;assign signedVal to to the slot

	;pop all registers that were used ustring the procedure
	POP		ESI
	POP		EDI
	POP		EDX
	POP		ECX
	POP		EBX
	POP		EAX

	RET		24								;return 24 to clean up the stack of the passed parameters
ReadVal ENDP

; ---------------------------------------------------------------------------------
; Name: WriteVal
;
; The procedure processes the SDWORD numbers from userArray to compute the sum and average
; of the numbers in the array. Next it stores the sum, average, and all the numbers in userArray
; as string. Last, it invokes mDisplayString to print the the previously converted strings
;
; Preconditions: 
;	outputListStr, outputSumStr, and outputAvgStr, numListString, sumString, and sumString
;	are declared BYTE strings
;
; Postconditions: None because all registers are preserved by pushing and popping from the stack
;
; Receives: 
;	numListString [EBP+20]
;	sumString [EBP+12]
;	avgString [EBP+16]
;	outputListStr [EBP+24]
;	outputSumStr [EBP+28]
;	outputAvgStr [EBP+32]
;
; Returns:
;	numListString contains a string of all numbers in userArray
;	sumString stores totalSigned as a string
;	avgString stores averageSigned as a string
; ---------------------------------------------------------------------------------
WriteVal PROC

	LOCAL	totalSigned:SDWORD				;used to store the total of the numbers un userArray
	LOCAL	averageSigned:SDWORD			;average of the total
	LOCAL	integerLengthCounter:DWORD		;a counter used for reading and looping
	LOCAL	signTracker:DWORD				;used to determine if to write a negative valye or not

	;push all used registers to stack
	PUSH	EAX
	PUSH	EBX
	PUSH	ECX
	PUSH	EDX
	PUSH	EDI
	PUSH	ESI

; --------------------------
; The first major section of WriteVal is to get the total of the SDWORDS in userArray [EBP+8].
; A local SDWORD variable totalSigned is used add up all the values in userArray. Once
; everything is summed up, the next thing to check is whether it is a negative or not.
; If it is a poistive value, we move to _convertPositiveRemainders, else we move to 
; _convertNegativeRemainders. In both instances, we loop by dividing EAX (totalSigned)
; by 10 continuously until EAX reaches 0 (final quotient). Each loop pushes EDX (remainder)
; onto the stack. The next segments are _convertToPositiveString and _convertToNegativeString
; depending on if its negative or not. These loops pop EDX off the stack, converts it ASCII,
; and then stores it in current slot of EDI (sumString [EBP+12]). If the value is negative,
; the first byte of the string is a negative sign.
;---------------------------

;get the total of all the values in the userArray and store it in totalSigned
	MOV		totalSigned, 0					
	MOV		ECX, ARRAYSIZE					;ecx counter setup
	MOV		ESI, [EBP+8]					;ESI is loaded with address of userArray
_additionLoop:
	LODSD					
	ADD		totalSigned, EAX
	LOOP	_additionLoop					;load 4 bytes add it to totalSigned and then loop _additionLoop

	;compare whether total is negative or not
	MOV		integerLengthCounter, 0			;set integerLengthCounter to 0 used for counting the digits
	MOV		EAX, totalSigned				;move totalSigned to EAX, to begin dividing in the loops
	CMP		totalSigned, 0
	JL		_convertNegativeRemainders		;jump if the value is negative

;Loop continuously divides EAX by 10 until EAX is 0 (for postive integers)
_convertPositiveRemainders:
	MOV		EDX, 0
	MOV		EBX, 10							;10 is used to divide EAX by 10 to geth the last digit as a remainder
	CDQ
	IDIV	EBX
	PUSH	EDX								;PUSH the remainder from the stack
	INC		integerLengthCounter
	CMP		EAX, 0							
	JNE		_convertPositiveRemainders		;INC integerLengthCounter to use in next loop, countinue this loop until EAX is 0

	MOV		EDI, [EBP+12]					;assign sumString address to EDI

;Loop converts each pushed EDX that is popped to EAX into an ASCII value and stores it in current slot of EDI
_convertToPositiveString:
	POP		EAX
	ADD		EAX, 48							;converts digit to ASCII
	STOSB									;store the AL into current pointer of numString
	DEC		integerLengthCounter
	CMP		integerLengthCounter, 0
	JNE		_convertToPositiveString		;Loop continues until every digit is loaded into EDI
	MOV		EAX, 0
	STOSB									
	JMP		_getAverage						;null terminator and jump to _getAverage

;Loop continuously divides EAX by 10 until EAX is 0 (for negative integers)
_convertNegativeRemainders:
	MOV		EDX, 0
	MOV		EBX, 10							;10 is used to divide EAX by 10 to geth the last digit as a remainder
	CDQ
	IDIV	EBX
	NEG		EDX								
	PUSH	EDX								;EDX is negated to get a postive integer and then is stored on the stack
	INC		integerLengthCounter
	CMP		EAX, 0
	JNE		_convertNegativeRemainders		;INC integerLengthCounter to use in next loop, countinue this loop until EAX is 0

	MOV		EDI, [EBP+12]					
	MOV		EAX, 45
	STOSB									;assign sumString address to EDI and maked the first character a negative sign

;Loop converts each pushed EDX that is popped to EAX into an ASCII value and stores it in current slot of EDI
_convertToNegativeString:
	POP		EAX
	ADD		EAX, 48							;converts digit to ASCII
	STOSB									;store the AL into current pointer of numString
	DEC		integerLengthCounter
	CMP		integerLengthCounter, 0
	JNE		_convertToNegativeString		;Loop continues until every digit is loaded into EDI
	MOV		EAX, 0
	STOSB									;null terminator

; -------------------------
; The second major section of this procedure is to get the average of the totalSigned.
; We assign totalSigned to EAX and ARRAYSIZE to EBX, then divide by EBX to get the average.
; Once we have the average, we assign integerLengthCounter 0 and compare averageSigned to 0
; to see if the value is negative or postive. Depending on if its postive or negative, we go 
; to _avgDivPos or _avgDivNegStart. In either option we continuously divide EAX (average) by 10
; and push it onto the stack until EAX is 0. Next step involves popping the stack into EAX and
; loading each digit into ESI (avgString [EBP+8]) as an ASCII. If the integer is negative we 
; round down by 1, if the remainder is not 0, to get get the floor and add a negative sign.
; -------------------------

;get the average of averageSigned
_getAverage:

	MOV		averageSigned, 0				;assgin starting value of averageSigned
	MOV		EDX, 0
	MOV		EAX, totalSigned
	MOV		EBX, ARRAYSIZE					;assign totalSigned to EAX and ARRAYSIZE to EBX
	CDQ
	IDIV	EBX
	MOV		averageSigned, EAX				;div EAX by EBX to get the average

	MOV		integerLengthCounter, 0			;reset integerLengthCounter to 0
	MOV		EAX, averageSigned
	CMP		averageSigned, 0
	JL		_avgDivNegStart					;Move averageSigned to EAX and if less than 0 go to _avgDivNegStart

;Loop continuously divides EAX by 10 until EAX is 0 (for postive integers)
_avgDivPos:
	MOV		EDX, 0
	MOV		EBX, 10							;10 is used to divide EAX by 10 to geth the last digit as a remainder
	CDQ		
	IDIV	EBX
	PUSH	EDX								;PUSH the remainder from the stack
	INC		integerLengthCounter
	CMP		EAX, 0
	JNE		_avgDivPos						;INC integerLengthCounter to use in next loop, countinue this loop until EAX is 0
	
	MOV		EDI, [EBP+16]					;assign avgString address to EDI

;Loop converts each pushed EDX that is popped to EAX into an ASCII value and stores it in current slot of EDI
_convertAvgPosString:
	POP		EAX
	ADD		EAX, 48							;converts digit to ASCII
	STOSB									;store the AL into current pointer of avgString
	DEC		integerLengthCounter
	CMP		integerLengthCounter, 0
	JNE		_convertAvgPosString			;Loop continues until every digit is loaded into EDI
	MOV		EAX, 0
	STOSB									
	JMP		_convertArrayString				;null terminator jump to next step

;check whether the remainder in original divsion is equal to 0, if not sub 1 to floor the value
_avgDivNegStart:
	CMP		EDX, 0
	JE		_avgDivNeg
	SUB		EAX, 1

;Loop continuously divides EAX by 10 until EAX is 0 (for negative integers)
_avgDivNeg:
	MOV		EDX, 0
	MOV		EBX, 10							;10 is used to divide EAX by 10 to geth the last digit as a remainder
	CDQ		
	IDIV	EBX								
	NEG		EDX	
	PUSH	EDX								;EDX is negated to get a postive integer and then is stored on the stack
	INC		integerLengthCounter
	CMP		EAX, 0					
	JNE		_avgDivNeg						
	
	MOV		EDI, [EBP+16]
	MOV		EAX, 45
	STOSB									;assign avgString address to EDI and maked the first character a negative sign

_convertAvgNegString:
	POP		EAX
	ADD		EAX, 48							;converts digit to ASCII
	STOSB									;store the AL into current pointer of avgString
	DEC		integerLengthCounter
	CMP		integerLengthCounter, 0
	JNE		_convertAvgNegString			;Loop continues until every digit is loaded into EDI
	MOV		EAX, 0
	STOSB									;null terminator
	
; -------------------------
; The third major section of this procedure converts the SWDWORDs in userArray
; into strings and store them in numListString. It first does this by checks to 
; see if the number is negative and if so changes signTracker to 1. Next portion
; is the division loop to continuously divide by 10 and pushing the remainders 
; to stack until EAX is 0. Last step to pop the remainders from the stack into
; EAX and loading them into numListString. This entil section repeats until 
; ECX reaches 0
; -------------------------

;load all necassary variables into the the needed registers
_convertArrayString:	
	MOV		ECX, ARRAYSIZE					;ecx counter setup
	MOV		ESI, [EBP+8]					;userArray
	MOV		EDI, [EBP+20]					;numListString

;this is the main giany loop that stores all SDWORD integers from userArray to numListArray
_startArrayString:
	LODSD									;load current userArray variable into EAX
	MOV		signTracker, 0
	MOV		integerLengthCounter, 0
	CMP		EAX, 0							
	JGE		_remainderLoop
	MOV		signTracker, 1					;compare EAX to 0 and if EAX is negative set signTrack to 1

;the remainderLoop continuously divides EAX by 10 until EAX is 0, which pushing remainders to the stack
_remainderLoop:
	MOV		EDX, 0
	MOV		EBX, 10							;10 is used to divide EAX by 10 to geth the last digit as a remainder
	CDQ		
	IDIV	EBX
	CMP		signTracker, 1
	JNE		_noNegation
	NEG		EDX								;if signTracker is 1 then negate EDX before pushing to the stack
_noNegation:
	PUSH	EDX								;PUSH the remainder from the stack
	INC		integerLengthCounter
	CMP		EAX, 0
	JNE		_remainderLoop					;inc integerLengthCounter and if EAX is 0 leave loop

	;if signTracker is 1, store negative sign as the first BYTE
	CMP		signTracker, 1
	JNE		_convertToString
	MOV		EAX, 45
	STOSB

;this s final step to convert the current integer to a string
_convertToString:
	POP		EAX
	ADD		EAX, 48							;converts digit to ASCII
	STOSB									;store AL in current pointer of numListString
	DEC		integerLengthCounter
	CMP		integerLengthCounter, 0
	JNE		_convertToString
	CMP		ECX, 1							;if last SDWORD in array do not add ASCII 44 and 32
	JE		_finishLoop
	MOV		EAX, 44						
	STOSB	
	MOV		EAX, 32
	STOSB									;if another number is ging to be stored in numListString store a comma and space in the next two slots of numListString
_finishLoop:
	LOOP	_startArrayString

	;print everything using mDisplayString macro
	mDisplayString [EBP+20], [EBP+12], [EBP+16], [EBP+24], [EBP+28], [EBP+32]

	;pop all used registers off the stack
	POP		ESI
	POP		EDI
	POP		EDX
	POP		ECX
	POP		EBX
	POP		EAX

	RET		28								;return 28 to clear stack
WriteVal ENDP

END main

