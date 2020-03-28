<%@ page import='java.io.*' %>
<%@ page import='java.util.*' %>
<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="session" />


<%
String ret = etalisIO.query("retractall(trRules(_)),resetProlog.");
String content = request.getParameter("event_raw");
try
{
  // Here we'll write our data into a file called
  // sample.txt, this is the output.
  File file = new File("C:/Documents and Settings/Administrator/workspace/etalis/current_event.event");
  
  // We'll write the string below into the file
  String data = content;
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

StringBuilder contents = new StringBuilder();

try {
  //use buffering, reading one line at a time
  //FileReader always assumes default encoding is OK!
  File file = new File("C:/Documents and Settings/Administrator/workspace/etalis/current_event.event");
  BufferedReader input =  new BufferedReader(new FileReader(file));
  try {
    String line = null; //not declared within while loop
    /*
    * readLine is a bit quirky :
    * it returns the content of a line MINUS the newline.
    * it returns null only for the END of the stream.
    * it returns an empty String if two newlines appear in a row.
    */
    while (( line = input.readLine()) != null){
      contents.append(line);
      contents.append(System.getProperty("line.separator"));
    }
  }
  finally {
    input.close();
  }
}
catch (IOException ex){
  ex.printStackTrace();
}


etalisIO.loadEventFile("C:/Documents and Settings/Administrator/workspace/etalis/current_event.event");
response.setContentType("text/html");
response.setHeader("Cache-Control", "no-cache");
etalisIO.query("retractall(out(_)).");
String outp = contents.toString();
outp = outp.replaceAll("\n", "<br>");
outp = "<html><head><link rel=\"stylesheet\" href=\"iframe.css\"></head><body>"  + outp + "</body></html>";
response.getWriter().write(outp);


%>
