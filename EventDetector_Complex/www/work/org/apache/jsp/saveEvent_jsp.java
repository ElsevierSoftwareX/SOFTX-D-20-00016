package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.io.*;
import java.util.*;

public final class saveEvent_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  private javax.el.ExpressionFactory _el_expressionfactory;
  private org.apache.AnnotationProcessor _jsp_annotationprocessor;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspInit() {
    _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
    _jsp_annotationprocessor = (org.apache.AnnotationProcessor) getServletConfig().getServletContext().getAttribute(org.apache.AnnotationProcessor.class.getName());
  }

  public void _jspDestroy() {
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("\r\n");
      com.etalis.ioEtalis etalisIO = null;
      synchronized (session) {
        etalisIO = (com.etalis.ioEtalis) _jspx_page_context.getAttribute("etalisIO", PageContext.SESSION_SCOPE);
        if (etalisIO == null){
          etalisIO = new com.etalis.ioEtalis();
          _jspx_page_context.setAttribute("etalisIO", etalisIO, PageContext.SESSION_SCOPE);
        }
      }
      out.write("\r\n");
      out.write("\r\n");
      out.write("\r\n");

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



      out.write('\r');
      out.write('\n');
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try { out.clearBuffer(); } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
