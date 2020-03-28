package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class help_jsp extends org.apache.jasper.runtime.HttpJspBase
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

      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("<script type=\"text/javascript\" src=\"tabber.js\"></script>\r\n");
      out.write("<link rel=\"stylesheet\" href=\"example.css\" TYPE=\"text/css\" MEDIA=\"screen\">\r\n");
      out.write("<link rel=\"stylesheet\" href=\"color-scheme.css\" TYPE=\"text/css\" MEDIA=\"screen\">\r\n");
      out.write("<link rel=\"stylesheet\" href=\"bluehaze.css\" TYPE=\"text/css\" MEDIA=\"screen\">\r\n");
      out.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("<div id=\"header\">\r\n");
      out.write("      <a style=\"text-decoration:none\" class=\"headerTitle\" chref=\"/\">ETALIS</a>\r\n");
      out.write("      :: Event-driven Transaction Logic Inference System<br>\r\n");
      out.write("    </div>\r\n");
      out.write("\r\n");
      out.write("<div class=\"sideBox LHS\">\r\n");
      out.write("      <div>Main menu</div>\r\n");
      out.write("\t       \t<a href=\"/\">Main</a>\t\r\n");
      out.write("\t        <a href=\"help.jsp\">Help</a>\r\n");
      out.write("\t        <a href=\"contact.html\">Contact</a>\r\n");
      out.write("\t        <a href=\"http://code.google.com/p/etalis/downloads/list\">Foundations</a>\r\n");
      out.write("\t        <a href=\"http://code.google.com/p/etalis/source/browse/\">SVN repository</a>\r\n");
      out.write("\t        <a href=\"http://www.gnu.org/licenses/lgpl-3.0.txt\">License</a>\r\n");
      out.write("\t        <a href=\"devS.html\">Team</a>     \r\n");
      out.write("\t    </div>\r\n");
      out.write("\t\t<div id=\"bodyText\">\r\n");
      out.write("\t\t<!-- \r\n");
      out.write("\t\t<p>\r\n");
      out.write("\t\tTo use the engine , you must first load a pattern using the \"event management\" tab , you can \r\n");
      out.write("\t\teither write your own script , use the default one or upload an ASCII file containing the patterns.\r\n");
      out.write("\t\tYou could then click on the compile button and go to the \"interactive console\" to execute queries against\r\n");
      out.write("\t\tyour event file.\r\n");
      out.write("\t\tQueries must be valid , otherwise you will get an exception from the backend prolog engine .\r\n");
      out.write("\t\tExamples of queries include ,but not restricted to :<br> \r\n");
      out.write("\t\t<b>event(event_name) </b>  :: fires an event // note that event_name should not have any spaces nor should \r\n");
      out.write("\t\tit begin with a capital letter , it can be of any complexity like :<br>\r\n");
      out.write("\t\t\t<u>event(t1).</u>  <br>\r\n");
      out.write("\t\t\t<u>event(stock('google',11,123.2)). </u><br> \r\n");
      out.write("\t\t\t<u>event(t1,[time(2009,2,10,05,12,00),time(2009,2,10,05,12,1)]).</u><br>\r\n");
      out.write("\t\t\tQueries may also be :<br>\r\n");
      out.write("\t\t\t<u>retractall(event(_)).</u> // delete all events from the data base.   <br>\r\n");
      out.write("\t\t\t<u>assert(new_pattern).</u> // assert a new pattern , note that the program can change it self .<br>\r\n");
      out.write("\t\t\t<p>It is also possible to combine queries in the same command using commas , example : <br>\r\n");
      out.write("\t\t\tevent(a),event(b),event(c). // this should fire a , then b and finally c .<br>\r\n");
      out.write("\t\t</p></p>\r\n");
      out.write("\t\t -->\r\n");
      out.write("\r\n");
      out.write("<code>ETALIS</code>\r\n");
      out.write("\r\n");
      out.write("\t\t<p>\r\n");
      out.write("\t\t<b>ETALIS</b> is an open source engine for Event Processing and reactivity handling. The engine is \r\n");
      out.write("\t\tbased on a logic semantics, specified in a language Concurrent Transaction Logic for Events \r\n");
      out.write("\t\t(CTR-E). Due to its logic root, ETLAIS also supports reasoning about events, context, and \r\n");
      out.write("\t\tcomplex situations.\r\n");
      out.write("\t\t</p>\r\n");
      out.write("\t\t<p>\r\n");
      out.write("\t\t<b>Tab #1 (Event File Management).</b> In this tab a user can load an event program (event patterns of \r\n");
      out.write("\t\tinterest) into ETALIS. A couple of examples have been provided to show the user the syntax of \r\n");
      out.write("\t\tCTR-E (that is understandable by ETALIS). Provided complex event patterns can be edited directly \r\n");
      out.write("\t\tin the pane, i.e., can be extended, modified or completely removed. If a user wants to use her/his \r\n");
      out.write("\t\town event program, event patterns should be saved in a file with an extension *.event, and uploaded \r\n");
      out.write("\t\tto ETALIS. Either a typed event program, or uploaded one, needs to be compiled and loaded in the \r\n");
      out.write("\t\tsystem. By pressing \"Compile and Load\", an event program is ready for the execution. \r\n");
      out.write("\t\t</p>\r\n");
      out.write("\t\t<p>\r\n");
      out.write("\t\t<b>Tab #2 (Interactive Console).</b> Using this tab, a user can directly interact with ETALIS. The goal of \r\n");
      out.write("\t\tthis demo is to show how the engine, for user triggered events, computes complex events. Complex \r\n");
      out.write("\t\tevents (event program) need to be compiled and loaded into the engine (see Tab #1). For a given event \r\n");
      out.write("\t\tprogram, a user can generate a sequence of events and observe how complex patterns are being detected \r\n");
      out.write("\t\tin real time. An event 'e0' can be triggered by typing the following command in the text box and \r\n");
      out.write("\t\tpressing 'ENTER':\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\t<code>event(t0).</code>   \r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\tFor instance, if we want to detect a complex event: complexEvent0 :- t1 * t2 * t3 (that represents a \r\n");
      out.write("\t\tsequence of an event t1, followed by t2, followed by t3), we need to execute following commands: \r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\t<code>event(t1).</code><br>\r\n");
      out.write("\t\t<code>event(t2).</code><br>\r\n");
      out.write("\t\t<code>event(t3).</code><br>\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\tFor each triggered event there will be a time stamp automatically assigned to. An event has the following \r\n");
      out.write("\t\tform:\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\t<code>event(evName, (T1, T2)(X1,...,Xn))</code>\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\twhere :<br>\r\n");
      out.write("\t\t<ul>\r\n");
      out.write("\t\t<li>evName is a name (type) of an event;</li>\r\n");
      out.write("\t\t<li><code>(T1, T2)</code> is an interval on which an event is defined ;</li>\r\n");
      out.write("\t\t<li><code>(X1,...,Xn)</code> is a list of attributes (data) carried by an event.</li>\r\n");
      out.write("\t\t</ul>\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\tThe interval is defined by <code>T1</code> and <code>T2</code>, where each of them contains data, time and a time point. For example, \r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\t<code>(event(a, (datime(2009, 7, 8, 1, 1, 1, 1), datime(2009, 7, 8, 1, 1, 1, 1))).</code> \r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\tdenotes that an event 'a' occurred on 8th July 2009, at 01:01. The last number denotes relative position \r\n");
      out.write("\t\tbetween triggered events (to enable a fine grained time resolution). These time points are needed to \r\n");
      out.write("\t\tdistinguish between events that happened in intervals less than 1 microsecond. For instance, if events, \r\n");
      out.write("\t\t'a' and 'b', happened 1 nanosecond one after another, a time point n will be assigned to 'a', and n+1 to 'b'.\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\tAfter each triggered event, ETALIS will display its occurrence in the execution pane. Additionally the \r\n");
      out.write("\t\tengine will trigger intermediate events and complex events (when they occur). For more details on computation \r\n");
      out.write("\t\tof intermediate and complex events, a user is referred to 'Foundations' section of ETLAIS. \r\n");
      out.write("\t\t</p>\r\n");
      out.write("\t\t<p>\r\n");
      out.write("\t\t<b>Tab #3 (Google Stocks Demo):</b> ETLAIS is connected to Google finance web service that provides live stock data \r\n");
      out.write("\t\tfor a number of companies Worldwide. Currently, Google provides stock data refreshed every second (higher \r\n");
      out.write("\t\tfrequency of stock events is, at present, not possible). Additionally when the stock exchange is closed, \r\n");
      out.write("\t\tprices are not changing. To be able to show the demo (working all the time, not only when the stock exchange \r\n");
      out.write("\t\tis open), we have created an example patterns that calculate certain aggregate functions on stock events. \r\n");
      out.write("\t\tParticularly the average price is calculated for Google stocks in an interval defined by 'start' and 'stop' \r\n");
      out.write("\t\tuser triggered events. \r\n");
      out.write("\t\t</p>\r\n");
      out.write("\t\t<p>\r\n");
      out.write("\t\t<b>Tab #3 (Test with Synthetic Events):</b> In this demo, a user can load an event program (set of complex patterns) \r\n");
      out.write("\t\tand executed it against a stream of synthetic events. An artificially created stream of events can be generated \r\n");
      out.write("\t\tby providing two parameters, the number of distinguished event types contained in the stream and the stream \r\n");
      out.write("\t\tsize. The probability of appearance of an event type in the stream is equal for all events.\r\n");
      out.write("\t\t<br>\r\n");
      out.write("\t\tTo run the demo, a user needs to follow steps:<br>\r\n");
      out.write("\t\t<ol>\r\n");
      out.write("\t\t<li>load an event program in ETALIS (using Event File Management tab);</li>\r\n");
      out.write("\t\t<li>generate a synthetic event stream;</li>\r\n");
      out.write("\t\t<li>press 'Run' to execute the engine. ETLAIS will retrieve the time for which the input stream was handled w.r.t \r\n");
      out.write("\t\tgiven event program.</li>\r\n");
      out.write("\t\t<li>by pressing 'reset ETALIS' the engine will be reset from its current state, and a new test can possible be \r\n");
      out.write("\t\tperformed.</li>\r\n");
      out.write("\t\t</ol>\r\n");
      out.write("\t\t</p>\r\n");
      out.write("\t\t</div>\r\n");
      out.write("\t\t\r\n");
      out.write("    \r\n");
      out.write("</body>\r\n");
      out.write("</html>");
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
