package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.*;

public final class index_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  static {
    _jspx_dependants = new java.util.ArrayList(1);
    _jspx_dependants.add("/initSWI.jsp");
  }

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
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write('\n');
      out.write('\n');
      out.write('\n');
      com.etalis.ioEtalis etalisIO = null;
      synchronized (session) {
        etalisIO = (com.etalis.ioEtalis) _jspx_page_context.getAttribute("etalisIO", PageContext.SESSION_SCOPE);
        if (etalisIO == null){
          etalisIO = new com.etalis.ioEtalis();
          _jspx_page_context.setAttribute("etalisIO", etalisIO, PageContext.SESSION_SCOPE);
        }
      }
      out.write('\r');
      out.write('\n');
 
	etalisIO.init("etalisIO");
   etalisIO.query("resetProlog.");
   //etalisIO.loadEventFile("C:/Documents and Settings/Administrator/workspace/etalis/default_event.event");


      out.write('\n');
 int etalis_ver_major = 1; 
      out.write('\n');
      out.write('\n');
 int etalis_ver_minor = 0; 
      out.write('\n');
 String etalis_status = etalisIO.status();
      out.write(' ');
      out.write('\n');
 int etalis_debugging = 0; 
      out.write("\n");
      out.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\"http://www.w3.org/TR/html4/loose.dtd\">\n");
      out.write("\n");
      out.write("<HTML>\n");
      out.write("<HEAD>\n");
      out.write("<TITLE>ETALIS :: Event driven Transaction Logic Inference System</font></TITLE>\n");
      out.write("\n");
      out.write("<script type=\"text/javascript\" src=\"tabber.js\"></script>\n");
      out.write("<link rel=\"stylesheet\" href=\"example.css\" TYPE=\"text/css\" MEDIA=\"screen\">\n");
      out.write("<link rel=\"stylesheet\" href=\"color-scheme.css\" TYPE=\"text/css\" MEDIA=\"screen\">\n");
      out.write("<link rel=\"stylesheet\" href=\"bluehaze.css\" TYPE=\"text/css\" MEDIA=\"screen\">\n");
      out.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write("document.write('<style type=\"text/css\">.tabber{display:none;}<\\/style>');\n");
      out.write("</script>\n");
      out.write("\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write(" var req;\n");
      out.write("  function ajaxCall() {\n");
      out.write("   var poststr =\" encodeURI(document.liveQuery_form.liveQuery.value);\n");
      out.write("    var url = \"process.jsp\";\n");
      out.write("     if (window.XMLHttpRequest) {\n");
      out.write("      req = new XMLHttpRequest(); \n");
      out.write("      } \n");
      out.write("      else if (window.ActiveXObject) {\n");
      out.write("       req = new ActiveXObject(\"Microsoft.XMLHTTP\"); \n");
      out.write("       } \n");
      out.write("       req.open(\"GET\", url, true); \n");
      out.write("       req.onreadystatechange = callback; \n");
      out.write("       req.setRequestHeader(\"Content-Type\", \"application/x-www-form-urlencoded\"); \n");
      out.write("       req.setRequestHeader(\"Content-length\", poststr.length); \n");
      out.write("       req.setRequestHeader(\"Connection\", \"close\"); \n");
      out.write("       req.send(poststr); \n");
      out.write("       } \n");
      out.write("  function callback() { \n");
      out.write("  if (req.readyState == 4) { \n");
      out.write("  if (req.status == 200) { // update the HTML DOM based on whether or not message is valid \n");
      out.write("  parseMessage(); } } } \n");
      out.write("  function parseMessage() { \n");
      out.write("  \tvar message = req.responseText; \n");
      out.write("  \tsetMessage(message); } \n");
      out.write("  \tfunction setMessage(message) { \n");
      out.write("  \tmdiv = document.getElementById(\"OUTPUT_1\"); \n");
      out.write("  \tmdiv.innerHTML = message; } \n");
      out.write("</script>\n");
      out.write("<script language=javascript type='text/javascript'>\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("function refreshme() {window.frames[\"current_event_frame\"].location.reload();\n");
      out.write("window.frames[\"internal\"].location.reload();\n");
      out.write("}\n");
      out.write("\n");
      out.write("function refreshsyn(frame) {\n");
      out.write("\twindow.frames[frame].location.reload();\n");
      out.write("}\n");
      out.write("\n");
      out.write("function refreshOneSec(frame) {\n");
      out.write("\t\n");
      out.write("\tvar ctime = setTimeout(\"alert(\\\"refresh\\\");\",1000);\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\n");
      out.write("}\n");
      out.write("\n");
      out.write("function refreshstop(frame) {\n");
      out.write("\tclearTimeout(ctime);\t\n");
      out.write("}\n");
      out.write("</script>\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("</HEAD>\n");
      out.write("<BODY>\n");
      out.write("\n");
      out.write("<div id=\"header\">\n");
      out.write("      <a style=\"text-decoration:none\" class=\"headerTitle\" chref=\"/\">ETALIS</a>\n");
      out.write("      :: Event-driven Transaction Logic Inference System<br>\n");
      out.write("    </div>\n");
      out.write("\n");
      out.write("<div class=\"sideBox LHS\">\n");
      out.write("      <div>Main menu</div>\n");
      out.write("       \t<a href=\"/\">Main</a>\t\n");
      out.write("        <a href=\"help.jsp\">Help</a>\n");
      out.write("        <a href=\"contact.html\">Contact</a>\n");
      out.write("        <a href=\"http://code.google.com/p/etalis/downloads/list\">Foundations</a>\n");
      out.write("        <a href=\"http://code.google.com/p/etalis/source/browse/\">SVN repository</a>\n");
      out.write("        <a href=\"http://www.gnu.org/licenses/lgpl-3.0.txt\">License</a>\n");
      out.write("        <a href=\"devS.html\">Team</a>     \n");
      out.write("    </div>\n");
      out.write("<div id=\"bodyText\">\n");
      out.write("<div class=\"tabber\">\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\t<div class=\"tabbertab\">\n");
      out.write("\t<h3 > Event File Management </h3>\n");
      out.write("\t<div id =\"hideShow\";>\n");
      out.write("\t<form action=\"saveEvent.jsp\" method=\"get\" target=\"current_event_frame\">\n");
      out.write("\t<p>To test ETALIS, enter an event program in the textarea below. Alternatively you can browse and \n");
      out.write("    upload a file that contains an event program. Press \"Compile and Load\" to make the program ready \n");
      out.write("    for execution. To execute a program, go to \"Interactive Console\".\n");
      out.write("    For help on the ETALIS syntax, see <a href=\"help.jsp\">help</a></p>\n");
      out.write("\t<TEXTAREA NAME=\"event_raw\"; style=\"width: 100%; height:300px; background-color:#eee;\" VALIGN=\"top\" >\n");
      out.write("\t\n");
      out.write("%Examples of complex event patterns in ETALIS:\n");
      out.write("%=============================================\n");
      out.write("\n");
      out.write("%Sequence of events:\n");
      out.write("complexEvent0 :- t1 * t2 * t3.\n");
      out.write("\n");
      out.write("%Concurrent (synchronous) composition of events:\n");
      out.write("complexEvent1 :- (t2 * t4) # (t5 * t6).\n");
      out.write("\n");
      out.write("%Disjunction of events:\n");
      out.write("complexEvent2 :- t0 \\/ t1.\n");
      out.write("\n");
      out.write("%Sequence of events, combined with disjunction:\n");
      out.write("complexEvent3 :- (t1 * t2 * t3) \\/ (t4*t5).\n");
      out.write("\n");
      out.write("%Negation (with a sequence of events):\n");
      out.write("complexEvent4 :- (t5 * t6) cnot t7.\n");
      out.write("\t\n");
      out.write("\t</TEXTAREA><br><br>\n");
      out.write("\tSelect a file to upload an event program to ETALIS <br>\n");
      out.write("\t<INPUT TYPE=\"FILE\" NAME=\"event_file\" SIZE=\"64%\" > <br>\n");
      out.write("\t<INPUT TYPE=\"SUBMIT\" VALUE=\"Compile and Load \" onclick=\"refreshme()\" ><br>\n");
      out.write("\t</form></div>\t\n");
      out.write("\t<div id=\"OUTPUT_1\"></div>\t\n");
      out.write("\t</div>\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\t<div class=\"tabbertab\">\n");
      out.write("\t<h3> Interactive Console </h3>\n");
      out.write("\t<table border=\"1\" frame=\"void\" rules =\"none\" width=\"100%\"  >\n");
      out.write("\t<td width=\"47%\" valign=\"top\">\n");
      out.write("\t<u><b>Loaded Event Program:</b></u><br><br>\n");
      out.write("\t<iframe src=\"\" style=\"width: 100%; height: 270px\" name=\"current_event_frame\" marginwidth=\"0\" marginheight=\"0\" frameborder=\"0\" vspace=\"0\" hspace=\"0\"></iframe>\n");
      out.write("\t</td>\n");
      out.write("\t<td width=\"53%\" valign=\"top\">\n");
      out.write("\t<u><b>Execution:</b></u><br><br>\n");
      out.write("\t<iframe src=\"\" style=\"width: 100%; height: 300px\" name=\"internal\" marginwidth=\"0\" marginheight=\"0\" frameborder=\"0\" vspace=\"0\" hspace=\"0\"></iframe>\n");
      out.write("\t</td>\n");
      out.write("\t</table> \n");
      out.write("\t\n");
      out.write("\t<table border=\"1\" frame=\"void\" rules =\"none\">\n");
      out.write("\t<tr>\n");
      out.write("\t<td>\n");
      out.write("\t<FORM action =\"reset.jsp\" name =\"reset_form\" target = \"current_event_frame\" method=\"get\">\n");
      out.write("\t<INPUT TYPE=\"submit\" VALUE=\"reset ETALIS\" onclick=\"refreshme()\"></FORM>\n");
      out.write("\t</td>\n");
      out.write("\t<td>\n");
      out.write("\t<FORM action =\"clear.jsp\" name =\"liveQuery_form\" target = \"internal\" method=\"get\">\n");
      out.write("\t<INPUT TYPE=\"submit\" VALUE=\"clear screen\" onclick=\"refreshme()\"></FORM>\n");
      out.write("\t</td>\n");
      out.write("\t</table> \n");
      out.write("\t<br>\n");
      out.write("\t<FORM action =\"process.jsp\" name =\"liveQuery_form\" target = \"internal\" method=\"get\">\n");
      out.write("\tTo trigger an event, enter a statement, e.g., 'event(to)' and press ENTER.<br>\n");
      out.write("\tFor help on the ETALIS syntax for triggering an event, see <a href=\"help.jsp\">help</a><br>\n");
      out.write("\t<!-- \n");
      out.write("\t<select name=\"query_list\">\n");
      out.write("\t\t<option value=\"fire\">fire () </option>\n");
      out.write("\t\t<option value=\"void\"> () </option>\n");
      out.write("  \t\t<option value=\"trace\">trace.</option>\n");
      out.write("  \t\t<option value=\"db_out\">db(Out).</option>\n");
      out.write("  \t\t<option value=\"halt\">halt.</option>,\n");
      out.write("\t</select>\n");
      out.write("\t<INPUT TYPE=\"TEXT\" NAME=\"liveQuery\" SIZE=\"60%\" > \n");
      out.write("\t<input type=\"radio\" name=\"logradio\" value=\"raw\" checked> Show raw Log\n");
      out.write("\t<input type=\"radio\" name=\"logradio\" value=\"fired\" > Show fired Events<br>\n");
      out.write("\t -->\n");
      out.write("\t <INPUT TYPE=\"TEXT\" NAME=\"liveQuery\" SIZE=\"60%\" > \n");
      out.write("\t</FORM>\n");
      out.write("\t</div>\n");
      out.write("\t\n");
      out.write("\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\t\n");
      out.write("\t<div class=\"tabbertab\">\n");
      out.write("\t<h3> Google Stocks Demo </h3>\n");
      out.write("\t\t\t\n");
      out.write("\t\t\t<!--\n");
      out.write("\t\t\tUsed pattern :<br> \n");
      out.write("\t\t\t<iframe frameborder=\"0\" src=\"google.event\" height=\"130\" width=\"100%\" frameborder=\"1\"></iframe>\t\n");
      out.write("\t\t\t -->\n");
      out.write("\t\t\t\n");
      out.write("\t\t\t<p>ETALIS can apply aggregate functions while detecting complex events (in an incremental fashion).\n");
      out.write("\t\t\tAggregates over events are defined as <em>aggregate(+Template,+EventPath,-Result)</em>\n");
      out.write("\t\t\twhere <em>Template</em> can be any of the following: <em>count</em>, <em>sum(Var)</em>, \n");
      out.write("\t\t\t<em>min(Var)</em> , <em>max(Var)</em>. In the following example, ETALIS computes the average of \n");
      out.write("\t\t\tlive Google's stock prices in an interval delimited by two events: \n");
      out.write("\t\t\t<em>start_compEvent</em> and </em>stop_compEvent</em>.\t\n");
      out.write("\t\t\t<br><br>\t\t\n");
      out.write("\t<TEXTAREA NAME=\"google_example\"; style=\"width: 100%; height:300px; background-color:#eee;\" VALIGN=\"top\" >\n");
      out.write("%Examples of processing stock events from Google finance in ETALIS:\n");
      out.write("%==================================================================\n");
      out.write("\n");
      out.write("%Calculates number of events, triggered in the delimited interval:\n");
      out.write("counter_compEvent(Id,Counter):- \n");
      out.write("\t((db(company(Id)) * start_compEvent) * \n");
      out.write("\taggregate(count, stock(Id,Price,Volume)^* ,Counter) ) * \n");
      out.write("\tstop_compEvent.\n");
      out.write("\n");
      out.write("%Calculates the sum of prices in events from the delimited interval:\n");
      out.write("sum_compEvent(Id,Sum):- \n");
      out.write("\t((db(company(Id)) * start_compEvent) * \n");
      out.write("\taggregate(sum(Price), stock(Id,Price,Volume)^* ,Sum) ) * \n");
      out.write("\tstop_compEvent.\n");
      out.write("\n");
      out.write("%Calculates the avrage price of Google's stocks in the delimited interval:\n");
      out.write("avg(Id,Average):- \n");
      out.write("\t(counter_compEvent(Id,Counter) /\\ sum_compEvent(Id,Sum) ) * \n");
      out.write("\tprolog(is(Average,Sum/Counter)).\n");
      out.write("\n");
      out.write("% Selects companies from Google financial service to apply the above rules:\n");
      out.write("db(company('GOOG')).\n");
      out.write("\t\n");
      out.write("\t</TEXTAREA><br>\n");
      out.write("\t\t\t<table>\n");
      out.write("\t\t\tTest the Google Stock demo. Use \"Start\" and \"Stop\" to create an interval in which the avrage \n");
      out.write("\t\t\tprice of Google stocks will be calculated.<br>\n");
      out.write("\t\t\tTo reset the current state of the engine, press 'reset ETALIS'.<br>\n");
      out.write("\t\t\t\t<tr>\n");
      out.write("\t\t\t\t\t<td>\n");
      out.write("\t\t\t\t\t\t<form action=\"EtalisTest.jsp\" name=\"googledemo\" id=\"googledemo\" target=\"google_frame\" method=\"get\">\n");
      out.write("\t\t\t\t\t\t\t<input type=\"submit\" name=\"startgoogle\" value=\"Start\" onclick=\"\"/>\n");
      out.write("\t\t\t\t\t\t</form>\n");
      out.write("\t\t\t\t\t</td>\n");
      out.write("\t\t\t\t\t<td>\n");
      out.write("\t\t\t\t\t\t<form action=\"sendend.jsp\" name=\"sendend\" id=\"sendend\" target=\"google_frame\" method=\"get\">\n");
      out.write("\t\t\t\t\t\t\t<input type=\"submit\" name=\"endgoogle\" value=\"End\" onclick=\"refreshsyn(google_frame)\"/>\n");
      out.write("\t\t\t\t\t\t</form>\n");
      out.write("\t\t\t\t\t</td>\n");
      out.write("\t\t\t\t\t<td>\n");
      out.write("\t\t\t\t\t\t<form action=\"reset.jsp\" name=\"resetgoogle\" id=\"resetgoogle\" target=\"google_frame\" method=\"get\">\n");
      out.write("\t\t\t\t\t\t\t<input type=\"submit\" name=\"resetgoogle\" value=\"reset ETALIS\" onclick=\"refreshsyn(google_frame)\"/>\n");
      out.write("\t\t\t\t\t\t</form>\n");
      out.write("\t\t\t\t\t</td>\n");
      out.write("\t\t\t\t</tr>\n");
      out.write("\t\t\t</table>\t\t\n");
      out.write("\t\t<iframe frameborder=\"0\" src=\"\" name=\"google_frame\" id=\"google_frame\" height=\"200\" width=\"100%\" frameborder=\"1\"></iframe>\n");
      out.write("\t</div>\n");
      out.write("\n");
      out.write("\t<div class=\"tabbertab\">\n");
      out.write("\t<h3> Test with Synthetic Events</h3>\t\n");
      out.write("\t\n");
      out.write("\t<p>This demo demonstrates ETALIS capability to handle an event program (a set of event patterns) with\n");
      out.write("    respect to a given synthetically generated stream of events. To generate an input stream, set the number of \n");
      out.write("    distinguished event symbols and the number of total events in the stream. The achieved performance \n");
      out.write("    will be displayed in the right-hand side pane. \n");
      out.write("\t<table border=\"0\" width=\"100%\"  >\n");
      out.write("\t<tr>\n");
      out.write("\t\t<td valign=\"top\" width=\"50% align=\"left\">\n");
      out.write("\t\t<form action=\"genSynthetic.jsp\" name=\"genSynStream_form\" target=\"syn_frame\" method=\"get\">\n");
      out.write("\t\t\tNo. of distinguished event symbols n: [t0,...,tn]<br>\t\t\t\t\n");
      out.write("\t\t\t<input type=\"text\" name=\"numofparm\" id=\"numofparm\" value=\"5\"/><br>\t\t\t\t\n");
      out.write("\t\t\tStream Size<br>\t\t\t\t\n");
      out.write("\t\t\t<input type=\"text\" name=\"streamsize\" id=\"streamsiza\" value=\"1200\"><br>\t\t\t\n");
      out.write("\t\t\t<input type=\"submit\" name=\"synbutton\" value=\"Generate\" onclick=\"refreshsyn(syn_frame)\">\t\t\t\t\n");
      out.write("\t\t</form><br><hr width=\"85%\" align =\"left\">\n");
      out.write("\t\t<table>\n");
      out.write("\t\t\tTo load and compile an event program, use the 'Event File Management' tab.<br>\n");
      out.write("\t\t\tA loaded program will be executed against previously generated event stream<br>\n");
      out.write("\t\t\tby pressing 'Run'. To reset the current state of the engine, press 'reset ETALIS'.<br>\n");
      out.write("\t\t\t\t<tr>\n");
      out.write("\t\t\t\t\t<td>\n");
      out.write("\t\t\t\t\t\t<form action=\"runSyn.jsp\" name=\"runGenStream_form\" target=\"syn_frame\" method=\"get\">\n");
      out.write("\t\t\t\t\t\t\t<input type=\"SUBMIT\" name=\"synEvRun\" value=\"Run\"/>\n");
      out.write("\t\t\t\t\t\t\t<input type=\"checkbox\" name=\"synlog\" value=\"on\" checked=\"checked\"/> Run with Log\n");
      out.write("\t\t\t\t\t\t\t<input type=\"hidden\" name=\"synlog\" value=\"off\"/>\n");
      out.write("\t\t\t\t\t\t</form>\n");
      out.write("\t\t\t\t\t</td>\n");
      out.write("\t\t\t\t</tr>\n");
      out.write("\t\t\t\t<tr>\n");
      out.write("\t\t\t\t\t<td>\n");
      out.write("\t\t\t\t\t\t<form action=\"reset.jsp\" name=\"resetSyn\" id=\"resetSyn\" target=\"syn_frame\" method=\"get\">\t\t\t\n");
      out.write("\t\t\t\t\t\t\t<input type=\"submit\" name=\"resetgoogle\" value=\"reset ETALIS\" onclick=\"refreshsyn(syn_frame)\"/>\n");
      out.write("\t\t\t\t\t\t</form>\n");
      out.write("\t\t\t\t\t</td>\n");
      out.write("\t\t\t\t</tr>\n");
      out.write("\t\t\t</table>\n");
      out.write("\t\t\t\t\n");
      out.write("\t\t</td>\n");
      out.write("\t\t<td width=\"1\" bgcolor=\"#AAE\"><BR></td>\n");
      out.write("\t\t<td valign =\"top\"  >\n");
      out.write("\t\t<iframe src=\"\" name=\"syn_frame\" height=\"100%\" width=\"100%\" frameborder=\"0\"></iframe>\n");
      out.write("\t\t</td>\n");
      out.write("\t</tr>\n");
      out.write("\t</table>\n");
      out.write("\t</div>\n");
      out.write("</div>\n");
      out.write("<p>\n");
      out.write("Status         :: ");
      out.print(etalis_status);
      out.write("<BR>\n");
      out.write("ETALIS version :: ");
      out.print(etalis_ver_major );
      out.write('.');
      out.print(etalis_ver_minor );
      out.write(".alpha\n");
      out.write("</p>\n");
      out.write("</div>\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write("var gaJsHost = ((\"https:\" == document.location.protocol) ? \"https://ssl.\" : \"http://www.\");\n");
      out.write("document.write(unescape(\"%3Cscript src='\" + gaJsHost + \"google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E\"));\n");
      out.write("</script>\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write("try {\n");
      out.write("var pageTracker = _gat._getTracker(\"UA-3385668-4\");\n");
      out.write("pageTracker._trackPageview();\n");
      out.write("} catch(err) {}</script>\n");
      out.write("</BODY>\n");
      out.write("</HTML>\n");
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
