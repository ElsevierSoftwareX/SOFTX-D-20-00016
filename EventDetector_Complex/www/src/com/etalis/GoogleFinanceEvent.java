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

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;

//import java.util.Calendar;
//import java.util.Scanner;

public class GoogleFinanceEvent {
	static int counterTime=1;
	
		
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
		System.out.println(symbol);
		try {
			//Calendar ca = Calendar.getInstance();
			//String datime = "datime(" + ca.get(Calendar.YEAR) + "," + ( ca.get(Calendar.MONTH) + 1 ) + "," + ca.get(Calendar.DATE) + "," + ca.get(Calendar.HOUR_OF_DAY) + "," + ca.get(Calendar.MINUTE) + "," + ca.get(Calendar.SECOND) + "," + counterTime + ")";
			Query query=new Query("event(" + symbol + ",[" + counterTime + "," + counterTime + "])");
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
			System.out.println("Login success!");
		}
		try {
			String requestUrl = server + basePath + "default" + PORTFOLIO_FEED_URL_SUFFIX + "?returns=true&positions=true";
			int ntime = 5;
			int streamSize = ntime+1;
			Query startquery = new Query("event(start_compEvent,[0,0])");
			startquery.hasSolution();
			startquery.close();
			while(ntime > 0 ) {
				processFinanceDetail(service,requestUrl);
				//processFinanceDetail(service,requestUrl,sname);
				// to retrieve the data every 5 second
				Thread.sleep(1000);
				ntime--;
			}
			Query endquery = new Query("event(stop_compEvent,["+streamSize+","+streamSize+"])");
			endquery.hasSolution();
			endquery.close();
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
		Query queryRule = new Query("findall(GC,(eventFired(GC), GC =..[event,avg(X,Y),T]),L)");
		Compound result = (Compound)(queryRule.oneSolution().get("L"));
		return result.toString();
	}
	
}