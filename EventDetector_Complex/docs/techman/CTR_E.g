//
// ANTLR Grammar for the CTR-E language
//
grammar CTR_E;


//
// Reserves words:
//
tokens {
	SEQ='SEQ';
	AND='AND';
	OR='OR';
	PAR='PAR';
	EQUALS='EQUALS';
	MEETS='MEETS';
	DURING='DURING';
	STARTS='STARTS';
	FINISHES='FINISHES';

	NOT='NOT';
	WIN_TIME='WIN_TIME';
	DURATION_MODIFIER='@_duration';
	TIME_MODIFIER='@_datime';
}


//
// A CTR-E rule. Currently containing an event pattern. We might add conditions later.
//
rule
	:	prologPredicate ':-' pattern '.' EOF
	;
pattern
	:	windowedPattern (eventBinaryOperator pattern)?
	|	negatedPattern (eventBinaryOperator pattern)?
	|	event (eventBinaryOperator pattern)?
	;
windowedPattern
	:	'(' pattern ')' '.' windowSpecification

	;	
negatedPattern
	:	NOT '(' pattern ')' '[' pattern ',' pattern ']'
	;
absoluteTemporalEvent // example: "2010_01_01-12:00:00:000EST"@_datime
	:	StringLiteral TIME_MODIFIER
	;
event
	:	prologPredicate | absoluteTemporalEvent
	;	
eventBinaryOperator
	:	SEQ | AND | OR | PAR | EQUALS | MEETS | DURING | STARTS | FINISHES
	;
prologPredicate
	:	LowercaseIdentifier ('(' ((StringLiteral|NumericLiteral|prologVariable|prologFunction) (',' (StringLiteral|NumericLiteral|prologVariable|prologFunction))?)? ')')?
	;
prologVariable
	:	UppercaseIdentifier
	;
prologFunction
	:	LowercaseIdentifier '(' ((StringLiteral|NumericLiteral|prologVariable|prologFunction) (',' (StringLiteral|NumericLiteral|prologVariable|prologFunction))?)? ')'
	;
windowSpecification
	:	WIN_TIME '(' DURATION ')'
	;
DURATION // A relative time expression such as example: "1h20m"@_duration
	:	'"' (DecimalDigit+ ('y' | 'M' | 'd' | 'h' | 'm' | 's' | 'ms'))+ '"' DURATION_MODIFIER
	;


//
// Standard stuff
//
StringLiteral
	:	('"' StringChar* '"') | ('\'' StringChar* '\'')
	;
NumericLiteral
	:	DecimalLiteral | HexIntegerLiteral
	;
LowercaseIdentifier
	:	('a' .. 'f') ('0' .. '9' | 'A' .. 'Z' | 'a' .. 'z')*
	;
UppercaseIdentifier
	:	(('A' .. 'Z') | '_') ('0' .. '9' | 'A' .. 'Z' | 'a' .. 'z')*
	;
fragment StringChar
	:	UnicodeChar | EscapeSequence
	;
fragment UnicodeChar
	:	~('"' | '\\' | '\'')
	;
fragment EscapeSequence
	:	'\\' ('\"' | '\\' | '/' | 'b' | 'f' | 'n' | 'r' | 't' | 'u' HexDigit HexDigit HexDigit HexDigit)
	;
fragment HexIntegerLiteral
	:	'0' ('x' | 'X') HexDigit+
	;
fragment HexDigit
	:	('0' .. '9' | 'A' .. 'F' | 'a' .. 'f')
	;
fragment DecimalLiteral
	:	DecimalDigit+ '.' DecimalDigit* ExponentPart?
	|	'.'? DecimalDigit+ ExponentPart? ;
fragment DecimalDigit
	:	('0'..'9')
	;
fragment ExponentPart
	:	('e' | 'E') ('+' | '-') ? DecimalDigit+
	;
WS	:	 (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;}
	;

