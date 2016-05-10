package com.controller;

import android.app.Activity;
import android.net.wifi.WifiManager;
import android.util.Log;

import java.io.ByteArrayInputStream;
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
public class WifiHelper {
    WifiManager wManager;
    MainActivity myActivity;
    ActiveThread thread;
    PassiveThread passiveThread;
    ArrayBlockingQueue data;
    private boolean listenForConnections = true;

    private static final int PEER_PORT_NR = 50007;
    private static final int SERVER_PORT_NR = 49999;


    public WifiHelper(MainActivity mainActivity) {
        this.myActivity = mainActivity;
    }

    public void connectTo(String IP) {
        if (thread != null) {
            thread.stopThread();
        }
        thread = new ActiveThread(IP);
        data = new ArrayBlockingQueue<>(30);


        try {
            data.put((short) 5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        thread.start();

    }

    public void setNextData(short data) {
        try {
            this.data.put(data);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void startPassive() {
        passiveThread = new PassiveThread(thread.getSocket(), myActivity);
        passiveThread.start();
    }

    public void stopPassive() {
        passiveThread.stopThread();
    }

    /**
     * This thread can connect to a peer, exchange data, and send it to MainActivity
     */
    class ActiveThread extends Thread {
        String peerIp;
        Socket socket;

        /**
         * Constructor. Initializes thread
         *
         * @param ip The ip address to connect to
         */
        public ActiveThread(String ip) {
            peerIp = ip;
        }

        public Socket getSocket() {
            return socket;
        }

        /**
         * This runnable is the core of the thread. Preforms the actual network operations.
         */
        @Override
        @SuppressWarnings("unchecked")
        public void run() {
            try {
                //Set up socket and streams
                socket = new Socket(peerIp, PEER_PORT_NR);
                Log.i("myTag", "connected...");
                PrintStream oos = new PrintStream(socket.getOutputStream());
                DataInputStream ois = new DataInputStream(socket.getInputStream());

                //Send, and then receive data
                Log.i("myTag", "Transmitting and receiving...");
                while (true) {
                    try {
                        short temp = (short) data.take();
                        if (temp > 999) {
                            oos.print(4);
                            oos.print(temp);
                            Log.i("myTag", "" + temp);
                        } else if (temp < 1000 && temp > 100) {
                            oos.print(3);
                            oos.print(temp);
                            Log.i("myTag", "" + temp);
                        } else if (9 < temp && temp < 100) {
                            oos.print(2);
                            oos.print(temp);
                            Log.i("myTag", "" + temp);
                        } else if (0 < temp && temp < 10) {
                            oos.print(1);
                            oos.print(temp);
                            Log.i("myTag", "" + temp);
                        } else if (temp == 0) {
                            oos.print(1);
                            oos.print(1);
                        }
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    try {
                        sleep(20);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            } catch (IOException e) {

                Log.i("myTag", e.getMessage());
                e.printStackTrace();
            }
        }

        public void stopThread() {
            try {
                if (socket != null) {
                    socket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                interrupt();
            }
        }
    }

    class PassiveThread extends Thread {
        private Socket socket = null;
        private MainActivity mainActivity;
        private boolean connected = false;

        public PassiveThread(Socket socket, MainActivity activity) {
            this.socket = socket;
            mainActivity = activity;
        }

        @Override
        @SuppressWarnings("unchecked")
        public void run() {
            try {
                connected = true;
                DataInputStream dis = new DataInputStream(socket.getInputStream());

                while(true) {
                    int length = dis.readInt();
                    byte[] imageData = new byte[length];
                    dis.read(imageData, 0, length);

                    final byte[] imgData = imageData;
                    mainActivity.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mainActivity.receiveImageDataFromWifi(imgData);
                        }
                    });

                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        public void stopThread() {
            try {
                if (socket != null) {
                    socket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                interrupt();
            }
        }
    }
}
