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

import java.util.Calendar;
import java.util.Scanner;

public class Main {
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
		try {
			Calendar ca = Calendar.getInstance();
			String datime = "datime(" + ca.get(Calendar.YEAR) + "," + ( ca.get(Calendar.MONTH) + 1 ) + "," + ca.get(Calendar.DATE) + "," + ca.get(Calendar.HOUR_OF_DAY) + "," + ca.get(Calendar.MINUTE) + "," + ca.get(Calendar.SECOND) + "," + counterTime + ")";
			Query query=new Query("event(" + symbol + ",[" + datime + "," + datime + "])");
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
				for (int j = 0; j < inlinedFeed.getEntries().size(); j++) {
					PositionEntry positionEntry = inlinedFeed.getEntries().get(j);
					PositionData positionData = positionEntry.getPositionData();
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
	
	public static void main(String[] args) {
		JPL.init(); // create a SWI JPL engine. If you get an exception of jpl not found in your java.library.path then add to your system PATH variable the path: C:\Program Files\pl\bin for Windows or /usr/lib/swi-prolog/lib/i386 for linux
		// JPL for SWI
		Query query=new Query("consult('src/event_tr.P')");
		//Query query=new Query("consult('C:\\Documents and Settings\\danicic\\My Documents\\FZI\\Work\\Work on PhD\\etalis\\etalis\\src\\event_tr.P')");
		query.hasSolution();

		
		// or use Interprolog for XSB or SWI
		//PrologEngine engine;
		//engine = new XSBSubprocessEngine();
		//engine = new SWISubprocessEngine("swipl -G128M -L128M -T128M -A16M -nodebug -fnone -gset_prolog_flag(debug_on_error,false) -q",false,true);
		//engine.consultAbsolute(new File("E:\\workspaces\\etalis\\src\\event_tr.P"));
		//engine.consultAbsolute(new File("C:\\Documents and Settings\\danicic\\My Documents\\FZI\\Work\\Work on PhD\\etalis\\etalis\\src\\event_tr.P"));
		//engine.deterministicGoal("compile_events('C:\\Documents and Settings\\danicic\\My Documents\\FZI\\Work\\Work on PhD\\etalis\\etalis\\examples\\event_test_04.event')","[]",new Object[]{},"[]");
		
		System.out.println("Welcome to Etalis.\nPlease choose which test do you want to do:");
		System.out.println(" 1. Google Finance Event");
		System.out.println(" 2. Synthetic Event");
		System.out.print("Please enter your choice (you can input 1 or 2): ");
		Scanner sc = new Scanner(System.in);
		String inputCmd = sc.nextLine();
		if (inputCmd.equals("1")) { // do Google Finance Test
			String userEmail = "etalistest@googlemail.com";
			String userPassword = "12345678abc";
			String server = "http://finance.google.com";
			String basePath = "/finance/feeds/";
			String PORTFOLIO_FEED_URL_SUFFIX = "/portfolios";
			FinanceService service = new FinanceService("Google-PortfoliosDemo-1.0");
			
			Query query2 = new Query("compile_events('examples/event_test_15.event')");
			query2.hasSolution();
			
			if (!loginUser(service,userEmail,userPassword)) {
				System.out.println("Login Error, Please check the parameter.");
				System.exit(0);
			}
			else {
				System.out.println("Login success!");
			}
			try {
				String requestUrl = server + basePath + "default" + PORTFOLIO_FEED_URL_SUFFIX + "?returns=true&positions=true";
				int ntime = 10;
				while(ntime > 0 ) {
					processFinanceDetail(service,requestUrl);
					Thread.sleep(10000);
					ntime--;
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
		} else if (inputCmd.equals("2")) {
			// do Synthetic Test
			EventStream stream1 = new EventStream();
			stream1.generateEventStream(1, 0.5);
		} else {
			System.out.println("Your Input is not correct.");
		}
		// retrieve the results from Prolog
		System.out.println("\n  Retrieve the results from Prolog: ");
		Query queryRule=new Query("findall(eventFired(event(ce1(X,Y,Z),E)),eventFired(event(ce1(X,Y,Z),E)),L)");
		Compound result = (Compound)(queryRule.oneSolution().get("L"));
		System.out.println(result);
		System.out.println("Finish.");
		System.exit(0);
	}
}