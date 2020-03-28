<%@ page import='java.io.*' %>
<%@ page import='java.util.*' %>
<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="application" />
<html>
<head>
<link rel="stylesheet" href="iframe.css">
</head>
<body>
<% 
etalisIO.query_noOutput("retractall(trRules(_)),retractall(count(_)),retractall(counter(timeCounter,X)).");
etalisIO.query_noOutput("retractall(out(_))");
//this peace of code removes the contents of event file
try
{
  // Here we'll write our data into a file called
  // sample.txt, this is the output.
  File file = new File("C:/Documents and Settings/Administrator/workspace/etalis/current_event.event");
  
  // We'll write the string below into the file
  String data = "";
  Writer output = new BufferedWriter(new FileWriter(file));
  try {
      //FileWriter always assumes default encoding is OK!
      output.write( data );
    }
    finally {
      output.close();
    }
} catch (IOException e)
{
  e.printStackTrace();
}
response.setContentType("text/html");
response.setHeader("Cache-Control", "no-cache");
response.getWriter().write("");
%> 
</body></html>

