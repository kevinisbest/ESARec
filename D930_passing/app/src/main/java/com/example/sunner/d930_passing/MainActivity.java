package com.example.sunner.d930_passing;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {

    int bytesRead;
    Socket sock = null;
    Button bt_connect, bt_send1, bt_send2;
    EditText ipAddress;
    TextView status;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //set View物件
        bt_connect = (Button) findViewById(R.id.bt_connect);
        bt_send1 = (Button) findViewById(R.id.bt_send1);
        bt_send2 = (Button) findViewById(R.id.bt_send2);

        ipAddress = (EditText) findViewById(R.id.ip);
        status = (TextView) findViewById(R.id.textView1);

        bt_connect.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                connectDevice();
            }

        });

        bt_send1.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                sendProcess(Constants.IMAGE1_ADDR);
            }

        });

        bt_send2.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
                // TODO Auto-generated method stub
                sendProcess(Constants.IMAGE2_ADDR);
            }

        });
    }


    private void connectDevice() {
        Thread thread = new Thread() {
            @Override
            public void run() {
                super.run();

                //連接
                try {
                    Log.i(Constants.LLOG, "嘗試連接...");
                    sock = new Socket(ipAddress.getText().toString(), Constants.PORT_NUMBER);
                } catch (UnknownHostException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                if (sock == null)
                    Log.i(Constants.LLOG, "socket為空");
                else
                    Log.i(Constants.LLOG, "已連接");
            }
        };
        thread.start();
    }

    private void sendProcess(String imageName) {
        //File myFile = new File(Constants.IMAGE_ADDR);
        //byte[] mybytearray = new byte[(int) myFile.length()];
        FileInputStream fis = null;
        BufferedInputStream bis = null;
        OutputStream os = null;
        //try {
            //fis = new FileInputStream(myFile);
            bis = new BufferedInputStream(fis);

            //獲取輸出串流
            try {
                os = sock.getOutputStream();
            } catch (IOException e1) {
                // TODO Auto-generated catch block
                e1.printStackTrace();
            }

            //告知即將開始傳
            sendCommend(Constants.START_TO_SEND_IMAGE, os);

            //傳送圖片
            sendImage(imageName, os);

            //EL告知傳送結束
            sendCommend(Constants.END_SEND_IMAGE, os);



            //回收記憶體
            try {
                os.flush();
                //sock.close();
                bis.close();
                //sock = null;
                //status.setText("Socket is closed!");
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            /*
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        */
    }

    public void sendCommend(String commandString, OutputStream outputStream){
        //傳輸物件
        BufferedInputStream bis;
        byte[] mybytearray = commandString.getBytes();

        //向輸出串流寫入資訊
        try {
            outputStream.write(mybytearray, 0, mybytearray.length);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        status.setText("File was sent!");

        /*
        //回收記憶體
        try {
            bis.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        */
    }

    public void sendImage(String imageName, OutputStream outputStream){
        //傳輸物件
        File myFile = new File(imageName);
        BufferedInputStream bis = null;
        FileInputStream fis = null;
        byte[] mybytearray = new byte[(int) myFile.length()];

        //初始化串流
        try {
            fis = new FileInputStream(myFile);
            bis = new BufferedInputStream(fis);

            //檢查input stream是否為空
            if (bis == null)
                Log.e(Constants.LLOG, "buffer input stream為空");
            if (fis == null)
                Log.e(Constants.LLOG, "檔案input stream為空");


        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        //讀取檔案內容
        try {
            bytesRead = bis.read(mybytearray, 0, mybytearray.length);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        //向輸出串流寫入資訊
        try {
            outputStream.write(mybytearray, 0, mybytearray.length);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        status.setText("File was sent!");

        //回收記憶體
        try {
            bis.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
