package com.controller;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.view.View;
import android.widget.RadioGroup;
import android.widget.Toast;

import java.util.ArrayList;

import fragments.BigCarFragment;
import fragments.CamCarFragment;
import fragments.GrabCarFragment;
import fragments.MenuFragment;
import fragments.StartFragment;

public class MainActivity extends Activity {
    FragmentSwitcher switcher;
    int lastFragment;
    boolean isActivated;
    WifiHelper wHelper;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ArrayList<Fragment> fragments = new ArrayList<Fragment>();
        /*
         *  Add the fragments that should be contained at osme point in the container placed in this activity.
         */
        // The first screen that should be shown, added first here.
        fragments.add(new StartFragment()); // Place: 0
        //
        fragments.add(new CamCarFragment());// Place: 1
        fragments.add(new GrabCarFragment());// Place: 2
        fragments.add(new BigCarFragment());// Place: 3
        fragments.add(new MenuFragment());// Place: 4

        /*----------------------------------------*/


        switcher = new FragmentSwitcher(getFragmentManager(), findViewById(R.id.fragment_container), fragments);
        switcher.addFragment(0);
        isActivated = false;
        wHelper = new WifiHelper (this);
    }
    public WifiHelper getWifiHelper (){return wHelper;}

    public void openMenu (View v)
    {
        if (switcher.getCurrentFragment() instanceof CamCarFragment)
        {
            lastFragment = 1;
        }
        else if (switcher.getCurrentFragment() instanceof GrabCarFragment)
        {
            lastFragment = 2;
        }
        else if (switcher.getCurrentFragment() instanceof BigCarFragment)
        {
            lastFragment = 3;
        }

        switcher.switchTo(4); // Switch to menu_fragment.
    }
    public boolean getActivated(){return isActivated;}
    public void toggleSpecial(View v){
        if (isActivated)
            isActivated = false;
        else
            isActivated = true;
    }

    public void switchToCar(View v)
    {
        if (findViewById(R.id.cam_button) == v)
        {
            switcher.switchTo(1);
        }
        else if (findViewById(R.id.grab_button) == v)
        {
            wHelper.connectTo("grabcar");
            switcher.switchTo(2);


        }
        else if (findViewById(R.id.big_button) == v)
        {
            wHelper.connectTo("bigcar");
            switcher.switchTo(3);

        }
        else if (findViewById(R.id.start_button)== v)
        {
            RadioGroup rG = (RadioGroup)findViewById(R.id.radioGroup);
            if (rG.getCheckedRadioButtonId() == R.id.radioButton_Cam)
            {
                switcher.switchTo(1);
            }
            else if (rG.getCheckedRadioButtonId() == R.id.radioButton_grab)
            {
                wHelper.connectTo("grabcar");
                switcher.switchTo(2);

            }
            else if (rG.getCheckedRadioButtonId() == R.id.radioButton_big)
            {
                wHelper.connectTo("bigcar");
                switcher.switchTo(3);

            }
        }


    }

    public void goBack (View v)
    {
        switcher.switchTo(lastFragment);

    }

    public void sendToCar (String dataFrom , double data)
    {
        if(dataFrom == "HORIZONTAL")
        {


            if(data < 0)
            {
                if(getActivated() && switcher.getCurrentFragment() instanceof BigCarFragment )
                {
                    System.out.println("LEFT Activated: " + Math.abs(data));
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 256 + 128 + 512));
                }
                else
                {
                    System.out.println("LEFT: " + Math.abs(data));
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 256 + 128));

                }
            }

            else
            {
                if(getActivated() && switcher.getCurrentFragment() instanceof BigCarFragment)
                {
                    System.out.println("RIGHT: " + data);
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 128 + 512));
                }
                else
                {
                    System.out.println("RIGHT: " + data);
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 128));

                }
            }
        }
        else if (dataFrom == "VERTICAL")
        {
            if (getActivated() && switcher.getCurrentFragment() instanceof BigCarFragment)
            {
                if(data < 0)
                {
                    System.out.println("FORWARD: " + Math.abs(data));
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 256 + 512));
                }
                else
                {
                    System.out.println("BACKWARD: " + data);
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 512));
                }
            }
            else
            {
                if(data < 0)
                {
                    System.out.println("FORWARD: " + Math.abs(data));
                    wHelper.setNextData((short) (Math.abs(data) * 100 + 256 ));
                }
                else
                {
                    System.out.println("BACKWARD: " + data);
                    wHelper.setNextData((short) (Math.abs(data) * 100));
                }

            }
        }
    }

    public void receiveDataFromWifi (Object o)
    {

    }

    public int getLastFragment ()
    {
        return lastFragment;
    }
    @Override
    public void onBackPressed ()
    {
        if (switcher.getCurrentFragment() instanceof MenuFragment)
        {
            goBack(null);
        }
    }

}
