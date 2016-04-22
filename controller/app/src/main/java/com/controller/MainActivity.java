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

    public void switchToCar(View v)
    {
        if (findViewById(R.id.cam_button) == v)
        {
            switcher.switchTo(1);
        }
        else if (findViewById(R.id.grab_button) == v)
        {
            switcher.switchTo (2);
        }
        else if (findViewById(R.id.big_button) == v)
        {
            switcher.switchTo (3);
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
                switcher.switchTo(2);
                wHelper.connectTo("192.168.1.100");
            }
            else if (rG.getCheckedRadioButtonId() == R.id.radioButton_big)
            {
                switcher.switchTo(3);
            }
        }


    }

    public void goBack (View v)
    {
        switcher.switchTo(lastFragment);

    }

    public void sendToCar (short data)
    {
        wHelper.setNextData(data);
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
