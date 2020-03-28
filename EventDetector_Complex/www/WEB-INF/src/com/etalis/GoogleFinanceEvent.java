package com.etalis;

import com.google.gdata.data.extensions.Money;
import com.google.gdata.data.finance.PortfolioEntry;
import com.google.gdata.data.finance.PortfolioFeed;
import com.google.gdata.data.finance.PositionData;
import com.google.gdata.data.finance.PositionEntry;
import com.google.gdata.data.finance.PositionFeed;
import com.google.gdata.util.AuthenticationException;
import com.google.gdata.util.ServiceException;
import com.google.gdata.client.finance.FinanceService;

import jpl.JPL;
import jpl.Query;
import jpl.Compound;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.MalformedURLException;
import java.net.URL;

//import java.util.Calendar;
//import java.util.Scanner;

public class GoogleFinanceEvent {
	static int counterTime=1;
	int starttime = 0;
	static int stopflag = 1;
	private static Boolean loginUser(FinanceService service, String userID, String userPassword) {
		try {
			service.setUserCredentials(userID, userPassword);
		} catch (AuthenticationException e) {
			System.err.println("Invalid Credentials!");
			e.printStackTrace();
			return false;
		}
		return true;
	}

	private static void processEvent(String StockName, double nowPrice, double nowVolume) {
		String symbol = String.format("stock('%s',%.2f,%.0f)", StockName, nowPrice, nowVolume);
		//System.out.println(symbol);
		String event = "event(" + symbol + ",[" + counterTime + "," + counterTime + "])";
		//File temp = new File("C:/Documents and Settings/Administrator/workspace/etalis/src/examples/googleEvent.eventtmp");
		try {
			BufferedWriter temp = new BufferedWriter(new OutputStreamWriter(
	        		new FileOutputStream("C:/Documents and Settings/Administrator/workspace/etalis/googleEvent.eventtmp"
	        				,true)));
			temp.append(event);
			temp.append("\r");
			//System.out.println(event);
			temp.close();
		}catch(Exception ee) {
			ee.printStackTrace();
		}
		try {
			//Calendar ca = Calendar.getInstance();
			//String datime = "datime(" + ca.get(Calendar.YEAR) + "," + ( ca.get(Calendar.MONTH) + 1 ) + "," + ca.get(Calendar.DATE) + "," + ca.get(Calendar.HOUR_OF_DAY) + "," + ca.get(Calendar.MINUTE) + "," + ca.get(Calendar.SECOND) + "," + counterTime + ")";
			Query query=new Query(event);
			query.hasSolution();
			counterTime++;
		}catch (Exception ex) {
			ex.printStackTrace();
		}
	}
	
	private static void processFinanceDetail(FinanceService service, String feedUrl) throws IOException, MalformedURLException, ServiceException {
		double nowPrice = 0;
		double nowVolume = 0;
		PortfolioFeed portfolioFeed = service.getFeed(new URL(feedUrl), PortfolioFeed.class);
		for (int i = 0; i < portfolioFeed.getEntries().size(); i++) {
			PortfolioEntry portfolioEntry = portfolioFeed.getEntries().get(i);
			if (portfolioEntry.getFeedLink().getFeed() == null) {
			} else {
				PositionFeed inlinedFeed = portfolioEntry.getFeedLink().getFeed();
				//System.out.println(i);
				//System.out.println(portfolioEntry);
				//System.out.println(inlinedFeed);
				for (int j = 0; j < inlinedFeed.getEntries().size(); j++) {
					PositionEntry positionEntry = inlinedFeed.getEntries().get(j);
					PositionData positionData = positionEntry.getPositionData();
					//System.out.println(positionEntry);
					//System.out.println(positionData);
					for (int k = 0; k < positionData.getMarketValue().getMoney().size(); k++) {
					Money m = positionData.getMarketValue().getMoney().get(k);
						nowPrice = m.getAmount()/positionData.getShares();
						nowVolume = positionData.getShares();
					}
					String stockName = positionEntry.getSymbol().getSymbol();
					processEvent(stockName, nowPrice, nowVolume);
				}
			}
		}
	}
	
	private static void processFinanceDetail(FinanceService service, String feedUrl, String sname) throws IOException, MalformedURLException, ServiceException {
		double nowPrice = 0;
		double nowVolume = 0;
		String stockName;
		PortfolioFeed portfolioFeed = service.getFeed(new URL(feedUrl), PortfolioFeed.class);
		for (int i = 0; i < portfolioFeed.getEntries().size(); i++) {
			PortfolioEntry portfolioEntry = portfolioFeed.getEntries().get(i);
			if (portfolioEntry.getFeedLink().getFeed() == null) {
			} else {
				PositionFeed inlinedFeed = portfolioEntry.getFeedLink().getFeed();
				for (int j = 0; j < inlinedFeed.getEntries().size(); j++) {
					PositionEntry positionEntry = inlinedFeed.getEntries().get(j);
					stockName = positionEntry.getSymbol().getSymbol();
					if (sname == stockName) {
						PositionData positionData = positionEntry.getPositionData();
						for (int k = 0; k < positionData.getMarketValue().getMoney().size(); k++) {
						Money m = positionData.getMarketValue().getMoney().get(k);
							nowPrice = m.getAmount()/positionData.getShares();
							nowVolume = positionData.getShares();
						}
						processEvent(stockName, nowPrice, nowVolume);
					}						
					else
						continue;					
				}
			}
		}
	}
	
	public String executeEvent(String stockName) {
		//
		JPL.init();
		String sname = "GOOG"; //stockName

		Query query=new Query("consult('C:/Documents and Settings/Administrator/workspace/etalis/src/event_tr.P')");
		query.hasSolution();
		Query query1 = new Query("disable_order");
		query1.hasSolution();
		Query query2 = new Query("compile_events('C:/Documents and Settings/Administrator/workspace/etalis/google.event')");
		query2.hasSolution();
		//Query query3 = new Query("")
		/*		Query query3 = new Query("event(a,[1,1]),event(b,[2,2]),event(c,[3,3])");
		query3.hasSolution();*/

		String userEmail = "etalistest@googlemail.com";
		String userPassword = "12345678abc";
		String server = "http://finance.google.com";
		String basePath = "/finance/feeds/";
		String PORTFOLIO_FEED_URL_SUFFIX = "/portfolios";
		FinanceService service = new FinanceService("Google-PortfoliosDemo-1.0");
		
		
		if (!loginUser(service,userEmail,userPassword)) {
			System.out.println("Login Error, Please check the parameter.");
			System.exit(0);
		}
		else {
			//System.out.println("Login success!");
		}
		try {
			String requestUrl = server + basePath + "default" + PORTFOLIO_FEED_URL_SUFFIX + "?returns=true&positions=true";
			int ntime = 5;
			//int streamSize = ntime+1;
			int starttime;
			if (stopflag != 1) stopflag = 1;
			if (counterTime == 1) {
				starttime = counterTime - 1;
			}else starttime = counterTime;
			
			//int endtime= streamSize+ this.counterTime -1;
			
			Query startquery = new Query("event(start_compEvent,["+starttime+","+starttime+"])");
			startquery.hasSolution();
			startquery.close();
			while(stopflag > 0 ) {
				processFinanceDetail(service,requestUrl);
				//processFinanceDetail(service,requestUrl,sname);
				// to retrieve the data every 5 second
				Thread.sleep(1000);
				ntime--;
				if (stopflag == 0) break;
			}

		} catch (IOException e) {
			System.err.println("There was a problem communicating with the service.");
			e.printStackTrace();
		} catch (ServiceException e) {
			System.err.println("The server had a problem handling your request.");
			e.printStackTrace();
		} catch(Exception e){
			e.printStackTrace();
		}

		// retrieve the results from Prolog
		//System.out.println("\n  Retrieve the results from Prolog: ");
		//Query queryRule = new Query("findall(eventFired(event(avg(X,Y),[T1,T2])),eventFired(event(avg(X,Y),[T1,T2])),L)");
		//Query queryRule = new Query("findall(eventFired(X),eventFired(X),L)");
		Query querylog = new Query("findall(eventFired(X),(eventFired(X),X=..[event,stock(_,_,_),T]),M)");
		Compound stocklog = (Compound) (querylog.oneSolution().get("M"));
		String tmplog = this.formatString(stocklog.toString());
		Query query4 = new Query("enable_order");
		query4.hasSolution();
		//System.out.println(tmplog);
		return tmplog;
	}
	
	private String formatString(String raw) {
		String tmp = raw;
		//<div id="outstyle">
		tmp = tmp.replaceAll("','", "");
		tmp = tmp.replaceAll("'.'", "<br>");
		int gab = tmp.indexOf("[]");
		tmp = tmp.substring(0, gab);

		String tmp1 = "<html><head><link rel=\"stylesheet\" href=\"iframe.css\"></head><body>"  + tmp + "</body></html>";
		
		return tmp1;		
	}
	
	private static void resetCounter() {
		counterTime = 1;
	}
	
	public String sendStopEvent() {
		stopflag = 0;
		File ff = new File("C:/Documents and Settings/Administrator/workspace/etalis/googleEvent.eventtmp");
		ff.delete();
		Query endquery = new Query("event(stop_compEvent,["+counterTime+","+counterTime+"])");
		endquery.hasSolution();
		endquery.close();
		Query querylog = new Query("findall(eventFired(X),(eventFired(X),X=..[event,stock(_,_,_),T]),M)");
		Compound stocklog = (Compound) (querylog.oneSolution().get("M"));
		String tmplog = this.formatString(stocklog.toString());
		Query queryRule = new Query("findall(GC,(eventFired(GC), GC =..[event,avg(X,Y),T]),L)");
		Compound result = (Compound)(queryRule.oneSolution().get("L"));
		String tmp = result.toString();
		tmp = this.formatString(tmp);
		resetCounter();
		return tmplog+tmp;
	}
	
}