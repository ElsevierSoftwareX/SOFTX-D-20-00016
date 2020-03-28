<%@ page import="java.util.*"%>
<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@ include file="initSWI.jsp" %>
<% int etalis_ver_major = 1; %>

<% int etalis_ver_minor = 0; %>
<% String etalis_status = etalisIO.status();%> 
<% int etalis_debugging = 0; %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN""http://www.w3.org/TR/html4/loose.dtd">

<HTML>
<HEAD>
<TITLE>ETALIS :: Event driven Transaction Logic Inference System</font></TITLE>

<script type="text/javascript" src="tabber.js"></script>
<link rel="stylesheet" href="example.css" TYPE="text/css" MEDIA="screen">
<link rel="stylesheet" href="color-scheme.css" TYPE="text/css" MEDIA="screen">
<link rel="stylesheet" href="bluehaze.css" TYPE="text/css" MEDIA="screen">
<link rel="stylesheet" type="text/css" href="style.css" />
<script type="text/javascript">
document.write('<style type="text/css">.tabber{display:none;}<\/style>');
</script>

<script type="text/javascript">
 var req;
  function ajaxCall() {
   var poststr =" encodeURI(document.liveQuery_form.liveQuery.value);
    var url = "process.jsp";
     if (window.XMLHttpRequest) {
      req = new XMLHttpRequest(); 
      } 
      else if (window.ActiveXObject) {
       req = new ActiveXObject("Microsoft.XMLHTTP"); 
       } 
       req.open("GET", url, true); 
       req.onreadystatechange = callback; 
       req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"); 
       req.setRequestHeader("Content-length", poststr.length); 
       req.setRequestHeader("Connection", "close"); 
       req.send(poststr); 
       } 
  function callback() { 
  if (req.readyState == 4) { 
  if (req.status == 200) { // update the HTML DOM based on whether or not message is valid 
  parseMessage(); } } } 
  function parseMessage() { 
  	var message = req.responseText; 
  	setMessage(message); } 
  	function setMessage(message) { 
  	mdiv = document.getElementById("OUTPUT_1"); 
  	mdiv.innerHTML = message; } 
</script>
<script language=javascript type='text/javascript'>



function refreshme() {window.frames["current_event_frame"].location.reload();
window.frames["internal"].location.reload();
}

function refreshsyn(frame) {
	window.frames[frame].location.reload();
}

function refreshOneSec(frame) {
	
	var ctime = setTimeout("alert(\"refresh\");",1000);
	
	

}

function refreshstop(frame) {
	clearTimeout(ctime);	
}
</script>





</HEAD>
<BODY>

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
<div class="tabber">




	<div class="tabbertab">
	<h3 > Event File Management </h3>
	<div id ="hideShow";>
	<form action="saveEvent.jsp" method="get" target="current_event_frame">
	<p>To test ETALIS, enter an event program in the textarea below. Alternatively you can browse and 
    upload a file that contains an event program. Press "Compile and Load" to make the program ready 
    for execution. To execute a program, go to "Interactive Console".
    For help on the ETALIS syntax, see <a href="help.jsp">help</a></p>
	<TEXTAREA NAME="event_raw"; style="width: 100%; height:300px; background-color:#eee;" VALIGN="top" >
	
%Examples of complex event patterns in ETALIS:
%=============================================

%Sequence of events:
complexEvent0 :- t1 * t2 * t3.

%Concurrent (synchronous) composition of events:
complexEvent1 :- (t2 * t4) # (t5 * t6).

%Disjunction of events:
complexEvent2 :- t0 \/ t1.

%Sequence of events, combined with disjunction:
complexEvent3 :- (t1 * t2 * t3) \/ (t4*t5).

%Negation (with a sequence of events):
complexEvent4 :- (t5 * t6) cnot t7.
	
	</TEXTAREA><br><br>
	Select a file to upload an event program to ETALIS <br>
	<INPUT TYPE="FILE" NAME="event_file" SIZE="64%" > <br>
	<INPUT TYPE="SUBMIT" VALUE="Compile and Load " onclick="refreshme()" ><br>
	</form></div>	
	<div id="OUTPUT_1"></div>	
	</div>
	
	
	
	
	
	<div class="tabbertab">
	<h3> Interactive Console </h3>
	<table border="1" frame="void" rules ="none" width="100%"  >
	<td width="47%" valign="top">
	<u><b>Loaded Event Program:</b></u><br><br>
	<iframe src="" style="width: 100%; height: 270px" name="current_event_frame" marginwidth="0" marginheight="0" frameborder="0" vspace="0" hspace="0"></iframe>
	</td>
	<td width="53%" valign="top">
	<u><b>Execution:</b></u><br><br>
	<iframe src="" style="width: 100%; height: 300px" name="internal" marginwidth="0" marginheight="0" frameborder="0" vspace="0" hspace="0"></iframe>
	</td>
	</table> 
	
	<table border="1" frame="void" rules ="none">
	<tr>
	<td>
	<FORM action ="reset.jsp" name ="reset_form" target = "current_event_frame" method="get">
	<INPUT TYPE="submit" VALUE="reset ETALIS" onclick="refreshme()"></FORM>
	</td>
	<td>
	<FORM action ="clear.jsp" name ="liveQuery_form" target = "internal" method="get">
	<INPUT TYPE="submit" VALUE="clear screen" onclick="refreshme()"></FORM>
	</td>
	</table> 
	<br>
	<FORM action ="process.jsp" name ="liveQuery_form" target = "internal" method="get">
	To trigger an event, enter a statement, e.g., 'event(to)' and press ENTER.<br>
	For help on the ETALIS syntax for triggering an event, see <a href="help.jsp">help</a><br>
	<!-- 
	<select name="query_list">
		<option value="fire">fire () </option>
		<option value="void"> () </option>
  		<option value="trace">trace.</option>
  		<option value="db_out">db(Out).</option>
  		<option value="halt">halt.</option>,
	</select>
	<INPUT TYPE="TEXT" NAME="liveQuery" SIZE="60%" > 
	<input type="radio" name="logradio" value="raw" checked> Show raw Log
	<input type="radio" name="logradio" value="fired" > Show fired Events<br>
	 -->
	 <INPUT TYPE="TEXT" NAME="liveQuery" SIZE="60%" > 
	</FORM>
	</div>
	

	
	
	
	<div class="tabbertab">
	<h3> Google Stocks Demo </h3>
			
			<!--
			Used pattern :<br> 
			<iframe frameborder="0" src="google.event" height="130" width="100%" frameborder="1"></iframe>	
			 -->
			
			<p>ETALIS can apply aggregate functions while detecting complex events (in an incremental fashion).
			Aggregates over events are defined as <em>aggregate(+Template,+EventPath,-Result)</em>
			where <em>Template</em> can be any of the following: <em>count</em>, <em>sum(Var)</em>, 
			<em>min(Var)</em> , <em>max(Var)</em>. In the following example, ETALIS computes the average of 
			live Google's stock prices in an interval delimited by two events: 
			<em>start_compEvent</em> and </em>stop_compEvent</em>.	
			<br><br>		
	<TEXTAREA NAME="google_example"; style="width: 100%; height:300px; background-color:#eee;" VALIGN="top" >
%Examples of processing stock events from Google finance in ETALIS:
%==================================================================

%Calculates number of events, triggered in the delimited interval:
counter_compEvent(Id,Counter):- 
	((db(company(Id)) * start_compEvent) * 
	aggregate(count, stock(Id,Price,Volume)^* ,Counter) ) * 
	stop_compEvent.

%Calculates the sum of prices in events from the delimited interval:
sum_compEvent(Id,Sum):- 
	((db(company(Id)) * start_compEvent) * 
	aggregate(sum(Price), stock(Id,Price,Volume)^* ,Sum) ) * 
	stop_compEvent.

%Calculates the avrage price of Google's stocks in the delimited interval:
avg(Id,Average):- 
	(counter_compEvent(Id,Counter) /\ sum_compEvent(Id,Sum) ) * 
	prolog(is(Average,Sum/Counter)).

% Selects companies from Google financial service to apply the above rules:
db(company('GOOG')).
	
	</TEXTAREA><br>
			<table>
			Test the Google Stock demo. Use "Start" and "Stop" to create an interval in which the avrage 
			price of Google stocks will be calculated.<br>
			To reset the current state of the engine, press 'reset ETALIS'.<br>
				<tr>
					<td>
						<form action="EtalisTest.jsp" name="googledemo" id="googledemo" target="google_frame" method="get">
							<input type="submit" name="startgoogle" value="Start" onclick=""/>
						</form>
					</td>
					<td>
						<form action="sendend.jsp" name="sendend" id="sendend" target="google_frame" method="get">
							<input type="submit" name="endgoogle" value="End" onclick="refreshsyn(google_frame)"/>
						</form>
					</td>
					<td>
						<form action="reset.jsp" name="resetgoogle" id="resetgoogle" target="google_frame" method="get">
							<input type="submit" name="resetgoogle" value="reset ETALIS" onclick="refreshsyn(google_frame)"/>
						</form>
					</td>
				</tr>
			</table>		
		<iframe frameborder="0" src="" name="google_frame" id="google_frame" height="200" width="100%" frameborder="1"></iframe>
	</div>

	<div class="tabbertab">
	<h3> Test with Synthetic Events</h3>	
	
	<p>This demo demonstrates ETALIS capability to handle an event program (a set of event patterns) with
    respect to a given synthetically generated stream of events. To generate an input stream, set the number of 
    distinguished event symbols and the number of total events in the stream. The achieved performance 
    will be displayed in the right-hand side pane. 
	<table border="0" width="100%"  >
	<tr>
		<td valign="top" width="50% align="left">
		<form action="genSynthetic.jsp" name="genSynStream_form" target="syn_frame" method="get">
			No. of distinguished event symbols n: [t0,...,tn]<br>				
			<input type="text" name="numofparm" id="numofparm" value="5"/><br>				
			Stream Size<br>				
			<input type="text" name="streamsize" id="streamsiza" value="1200"><br>			
			<input type="submit" name="synbutton" value="Generate" onclick="refreshsyn(syn_frame)">				
		</form><br><hr width="85%" align ="left">
		<table>
			To load and compile an event program, use the 'Event File Management' tab.<br>
			A loaded program will be executed against previously generated event stream<br>
			by pressing 'Run'. To reset the current state of the engine, press 'reset ETALIS'.<br>
				<tr>
					<td>
						<form action="runSyn.jsp" name="runGenStream_form" target="syn_frame" method="get">
							<input type="SUBMIT" name="synEvRun" value="Run"/>
							<input type="checkbox" name="synlog" value="on" checked="checked"/> Run with Log
							<input type="hidden" name="synlog" value="off"/>
						</form>
					</td>
				</tr>
				<tr>
					<td>
						<form action="reset.jsp" name="resetSyn" id="resetSyn" target="syn_frame" method="get">			
							<input type="submit" name="resetgoogle" value="reset ETALIS" onclick="refreshsyn(syn_frame)"/>
						</form>
					</td>
				</tr>
			</table>
				
		</td>
		<td width="1" bgcolor="#AAE"><BR></td>
		<td valign ="top"  >
		<iframe src="" name="syn_frame" height="100%" width="100%" frameborder="0"></iframe>
		</td>
	</tr>
	</table>
	</div>
</div>
<p>
Status         :: <%=etalis_status%><BR>
ETALIS version :: <%=etalis_ver_major %>.<%=etalis_ver_minor %>.alpha
</p>
</div>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-3385668-4");
pageTracker._trackPageview();
} catch(err) {}</script>
</BODY>
</HTML>
