<html>
<head>
<script type="text/javascript" src="tabber.js"></script>
<link rel="stylesheet" href="example.css" TYPE="text/css" MEDIA="screen">
<link rel="stylesheet" href="color-scheme.css" TYPE="text/css" MEDIA="screen">
<link rel="stylesheet" href="bluehaze.css" TYPE="text/css" MEDIA="screen">
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<div id="header">
      <a style="text-decoration:none" class="headerTitle" chref="/">ETALIS</a>
      :: Event-driven Transaction Logic Inference System<br>
    </div>

<div class="sideBox LHS">
      <div>Main menu</div>
	       	<a href="/">Main</a>	
	        <a href="help.jsp">Help</a>
	        <a href="contact.html">Contact</a>
	        <a href="http://code.google.com/p/etalis/downloads/list">Foundations</a>
	        <a href="http://code.google.com/p/etalis/source/browse/">SVN repository</a>
	        <a href="http://www.gnu.org/licenses/lgpl-3.0.txt">License</a>
	        <a href="devS.html">Team</a>     
	    </div>
		<div id="bodyText">
		<!-- 
		<p>
		To use the engine , you must first load a pattern using the "event management" tab , you can 
		either write your own script , use the default one or upload an ASCII file containing the patterns.
		You could then click on the compile button and go to the "interactive console" to execute queries against
		your event file.
		Queries must be valid , otherwise you will get an exception from the backend prolog engine .
		Examples of queries include ,but not restricted to :<br> 
		<b>event(event_name) </b>  :: fires an event // note that event_name should not have any spaces nor should 
		it begin with a capital letter , it can be of any complexity like :<br>
			<u>event(t1).</u>  <br>
			<u>event(stock('google',11,123.2)). </u><br> 
			<u>event(t1,[time(2009,2,10,05,12,00),time(2009,2,10,05,12,1)]).</u><br>
			Queries may also be :<br>
			<u>retractall(event(_)).</u> // delete all events from the data base.   <br>
			<u>assert(new_pattern).</u> // assert a new pattern , note that the program can change it self .<br>
			<p>It is also possible to combine queries in the same command using commas , example : <br>
			event(a),event(b),event(c). // this should fire a , then b and finally c .<br>
		</p></p>
		 -->

<code>ETALIS</code>

		<p>
		<b>ETALIS</b> is an open source engine for Event Processing and reactivity handling. The engine is 
		based on a logic semantics, specified in a language Concurrent Transaction Logic for Events 
		(CTR-E). Due to its logic root, ETLAIS also supports reasoning about events, context, and 
		complex situations.
		</p>
		<p>
		<b>Tab #1 (Event File Management).</b> In this tab a user can load an event program (event patterns of 
		interest) into ETALIS. A couple of examples have been provided to show the user the syntax of 
		CTR-E (that is understandable by ETALIS). Provided complex event patterns can be edited directly 
		in the pane, i.e., can be extended, modified or completely removed. If a user wants to use her/his 
		own event program, event patterns should be saved in a file with an extension *.event, and uploaded 
		to ETALIS. Either a typed event program, or uploaded one, needs to be compiled and loaded in the 
		system. By pressing "Compile and Load", an event program is ready for the execution. 
		</p>
		<p>
		<b>Tab #2 (Interactive Console).</b> Using this tab, a user can directly interact with ETALIS. The goal of 
		this demo is to show how the engine, for user triggered events, computes complex events. Complex 
		events (event program) need to be compiled and loaded into the engine (see Tab #1). For a given event 
		program, a user can generate a sequence of events and observe how complex patterns are being detected 
		in real time. An event 'e0' can be triggered by typing the following command in the text box and 
		pressing 'ENTER':
		<br>
		<code>event(t0).</code>   
		<br>
		For instance, if we want to detect a complex event: complexEvent0 :- t1 * t2 * t3 (that represents a 
		sequence of an event t1, followed by t2, followed by t3), we need to execute following commands: 
		<br>
		<code>event(t1).</code><br>
		<code>event(t2).</code><br>
		<code>event(t3).</code><br>
		<br>
		For each triggered event there will be a time stamp automatically assigned to. An event has the following 
		form:
		<br>
		<code>event(evName, (T1, T2)(X1,...,Xn))</code>
		<br>
		where :<br>
		<ul>
		<li>evName is a name (type) of an event;</li>
		<li><code>(T1, T2)</code> is an interval on which an event is defined ;</li>
		<li><code>(X1,...,Xn)</code> is a list of attributes (data) carried by an event.</li>
		</ul>
		<br>
		The interval is defined by <code>T1</code> and <code>T2</code>, where each of them contains data, time and a time point. For example, 
		<br>
		<code>(event(a, (datime(2009, 7, 8, 1, 1, 1, 1), datime(2009, 7, 8, 1, 1, 1, 1))).</code> 
		<br>
		denotes that an event 'a' occurred on 8th July 2009, at 01:01. The last number denotes relative position 
		between triggered events (to enable a fine grained time resolution). These time points are needed to 
		distinguish between events that happened in intervals less than 1 microsecond. For instance, if events, 
		'a' and 'b', happened 1 nanosecond one after another, a time point n will be assigned to 'a', and n+1 to 'b'.
		<br>
		After each triggered event, ETALIS will display its occurrence in the execution pane. Additionally the 
		engine will trigger intermediate events and complex events (when they occur). For more details on computation 
		of intermediate and complex events, a user is referred to 'Foundations' section of ETLAIS. 
		</p>
		<p>
		<b>Tab #3 (Google Stocks Demo):</b> ETLAIS is connected to Google finance web service that provides live stock data 
		for a number of companies Worldwide. Currently, Google provides stock data refreshed every second (higher 
		frequency of stock events is, at present, not possible). Additionally when the stock exchange is closed, 
		prices are not changing. To be able to show the demo (working all the time, not only when the stock exchange 
		is open), we have created an example patterns that calculate certain aggregate functions on stock events. 
		Particularly the average price is calculated for Google stocks in an interval defined by 'start' and 'stop' 
		user triggered events. 
		</p>
		<p>
		<b>Tab #3 (Test with Synthetic Events):</b> In this demo, a user can load an event program (set of complex patterns) 
		and executed it against a stream of synthetic events. An artificially created stream of events can be generated 
		by providing two parameters, the number of distinguished event types contained in the stream and the stream 
		size. The probability of appearance of an event type in the stream is equal for all events.
		<br>
		To run the demo, a user needs to follow steps:<br>
		<ol>
		<li>load an event program in ETALIS (using Event File Management tab);</li>
		<li>generate a synthetic event stream;</li>
		<li>press 'Run' to execute the engine. ETLAIS will retrieve the time for which the input stream was handled w.r.t 
		given event program.</li>
		<li>by pressing 'reset ETALIS' the engine will be reset from its current state, and a new test can possible be 
		performed.</li>
		</ol>
		</p>
		</div>
		
    
</body>
</html>