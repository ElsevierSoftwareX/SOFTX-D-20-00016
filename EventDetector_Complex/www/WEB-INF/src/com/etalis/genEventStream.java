package com.etalis;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.LinkedHashSet;
import java.util.Random;
import java.util.Set;



public class genEventStream {
	private int streamSize;
	private int numofpar; // Number of Parameter
	private double oooPercentage;
	private String eventfileName;
	public float probabilityValue;
	public int symbol;
	public int counter;
	public int order;
	public int diffEvents;
	public BufferedWriter bw;
	public Random randGen1 = new Random(); 
	public Random randGen2 = new Random();
	public Set<Event> eventStream;
	
	public void gen(int streamSize, int numofpar, String fileName) {
		//
		try {
			this.generateEventStream(streamSize, 0, numofpar, fileName);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private void generateEventStream(int streamSize, double oooPercentage, int diffEvents, String fileName) throws IOException  {
		this.counter = streamSize;
		this.diffEvents = diffEvents;
		this.eventStream = new LinkedHashSet<Event>(streamSize);
		try {
			 if(oooPercentage < 0 || oooPercentage > 1) throw new Exception();
        } catch (Exception e) {
        	System.err.println("Invalid parameter for probability of out-of-order events: oooPercentage.");
			e.printStackTrace();
		}
        Event e;
        boolean duplicate;
        File ff = new File("C:/Documents and Settings/Administrator/workspace/etalis/src/examples/"+fileName);
        OutputStream os = new FileOutputStream(ff);
        os.write("".getBytes());
        os.close();
        //if (ff.exists()) ff.delete();
        //ff.createNewFile();
        
        //String etalisDir = System.getProperty("user.dir");
        bw = new BufferedWriter(new OutputStreamWriter(
        		new FileOutputStream(ff,true)));
        
    	for (int systemClock=1; systemClock<this.counter+1; systemClock++) {
    		symbol = randGen1.nextInt(this.diffEvents); // values: 0,1,2,...,diffEvents
    		probabilityValue = randGen2.nextFloat(); // values between 0 and 1
			if(probabilityValue <= oooPercentage){
				// Generate an out-of-order event;
				order = randGen2.nextInt(systemClock); // values: 1,2,...,systemClock-1;
				e = new Event(symbol, order);
			}else {
				// Generate an in-order event;
				e = new Event(symbol, systemClock);
			}
			// Eliminates events with duplicate time points.
			// As the stream is generated at designed time, this iteration is not a performance issue.
			duplicate = false;
			for(Event ev : this.eventStream){
				if(ev.timePoint == e.timePoint){
					this.counter++;
					duplicate = true;
				}
			}
			if(! duplicate){
				this.eventStream.add(e);
			}
        }
    	for(Event ev : this.eventStream){
			bw.append(ev.toString());
		}
        bw.close();
	}
	
	class Event{
		int symbol;
        int timePoint;

        public Event(){};

        public Event(int symbol, int timePoint){
            this.symbol = symbol;
            this.timePoint = timePoint;
        };

        public String toString() {
                StringBuilder buffer = new StringBuilder();
                //buffer.append("ooo_event(t"+this.symbol +",[");
                buffer.append("event(t"+this.symbol + ",[");
                buffer.append(this.timePoint);
                buffer.append(",");
                buffer.append(this.timePoint);
                buffer.append("]).\n");
                
        return buffer.toString();
        }
	}
	
}
