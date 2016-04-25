package com.controller;

import android.app.Activity;
import android.net.wifi.WifiManager;
import android.util.Log;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintStream;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Deque;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingDeque;

/**
 * Created by Carl-Henrik Hult on 2016-03-24.
 */
public class WifiHelper
{
    WifiManager wManager;
    MainActivity myActivity;
    ActiveThread activeThread;
    ArrayBlockingQueue data;
    private PassiveThread listenerThread;
    private boolean listenForConnections = true;

    private static final int PEER_PORT_NR = 50007;
    private static final int SERVER_PORT_NR = 49999;

    public WifiHelper (MainActivity mainActivity)
    {
        this.myActivity = mainActivity;
    }

    public void connectTo (String IP)
    {
        ActiveThread thread = new ActiveThread(IP);
        data = new ArrayBlockingQueue<>(30);

        try
        {
            data.put ((short)5);
        } catch(InterruptedException e)
        {
            e.printStackTrace();
        }
        thread.start();

    }

    public void setNextData (short data)
    {
        try
        {
            this.data.put(data);
        } catch(InterruptedException e)
        {
            e.printStackTrace();
        }
    }

    /**
     * Starts the thread that listens for incoming connections from peer
     */
    public void startThread()
    {
        if(listenerThread == null || !listenerThread.isAlive())
        {
            listenForConnections = true;
            listenerThread = new PassiveThread();
            listenerThread.start();
        }
    }

    /**
     * Stops the thread that listens for incoming connections from peer
     */
    public void stopThread()
    {
        listenForConnections = false;
        listenerThread.stopThread();
    }

    /**
     * This thread can connect to a peer, exchange data, and send it to MainActivity
     */
    private class ActiveThread extends Thread
    {
        String peerIp;

        /**
         * Constructor. Initializes thread
         * @param ip The ip address to connect to
         */
        public ActiveThread(String ip)
        {
            peerIp = ip;
        }

        /**
         * This runnable is the core of the thread. Preforms the actual network operations.
         */
        @Override
        @SuppressWarnings("unchecked")
        public void run()
        {
            try
            {
                //Set up socket and streams
                Socket socket = new Socket(peerIp, PEER_PORT_NR );
                Log.i("myTag", "connected...");
                PrintStream oos = new PrintStream(socket.getOutputStream());
                DataInputStream ois = new DataInputStream(socket.getInputStream());

                //Send, and then receive data
                Log.i("myTag", "Transmitting and receiving...");
                while (true)
                {
                    try{
                     short temp = (short)data.take();

                        if(temp > 255)
                        {
                            oos.print(2);
                            oos.print(temp);
                            Log.i("myTag", "" + temp);
                        }
                        else if( temp< 256)
                        {
                            oos.print(1);
                            oos.print(temp);
                            //Log.i("myTag", "" + temp);
                        }
                    }
                    catch(InterruptedException e)
                    {
                        e.printStackTrace();
                    }
                    try {
                        sleep(20);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                //final Object receivedData = ois.readShort();

                //Clean up
                /*oos.flush();
                oos.close();
                ois.close();
                socket.close();
*/
                //Handle received data
/*

                myActivity.runOnUiThread(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        myActivity.receiveDataFromWifi(receivedData);
                    }
                });
*/
            } catch(IOException e)
            {

                Log.i("myTag", e.getMessage());
                e.printStackTrace();
            }
        }
    }
    /**
     * This thread listens for a connection, exchanges data, and sends it to MainActivity
     */
    private class PassiveThread extends Thread
    {
        ServerSocket serverSocket = null;

        /**
         * This runnable is the core of the thread. Preforms the actual network operations.
         */
        @Override
        @SuppressWarnings("unchecked")
        public void run()
        {
            while(listenForConnections)
            {
                try
                {
                    //Set up socket
                    serverSocket = new ServerSocket();
                    serverSocket.setReuseAddress(true);
                    serverSocket.bind(new InetSocketAddress(PEER_PORT_NR));

                    //Accept connection and set up streams
                    Socket client = serverSocket.accept();
                    ObjectInputStream ois = new ObjectInputStream(client.getInputStream());
                    ObjectOutputStream oos = new ObjectOutputStream(client.getOutputStream());

                    //Receive, and then send data
                    Log.i("myTag", "Receiving and sending...");
                    final Object receivedData = ois.readObject();
                    oos.writeObject(null);

                    //Clean up
                    ois.close();
                    oos.flush();
                    oos.close();
                    client.close();
                    serverSocket.close();

                    myActivity.runOnUiThread(new Runnable()
                    {
                        @Override
                        public void run()
                        {
                            myActivity.receiveDataFromWifi(receivedData);
                        }
                    });
                }
                catch(IOException | ClassNotFoundException e)
                {
                    Log.i("myTag", e.getMessage());
                    e.printStackTrace();
                }
            }
        }

        /**
         * Interrupts the thread and stops it from listening for connections
         */
        public void stopThread()
        {
            try
            {
                if (serverSocket != null)
                {
                    serverSocket.close();
                }
            }
            catch(IOException e)
            {
                e.printStackTrace();
            }
            finally
            {
                interrupt();
            }
        }
    }
}
