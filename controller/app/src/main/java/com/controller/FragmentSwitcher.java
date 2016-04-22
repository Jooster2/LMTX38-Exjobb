package com.controller;

import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.view.View;

import com.controller.R;

import java.util.ArrayList;
/**
 * Created by Carl-Henrik Hult on 2016-03-23.
 */
public class FragmentSwitcher
{
    FragmentManager fM;
    View fragmentContainer;
    ArrayList <Fragment> allFragments;
    public FragmentSwitcher (FragmentManager fragManager, View container, ArrayList <Fragment> allFragments)
    {
        fM = fragManager;
        fragmentContainer = container;
        this.allFragments = allFragments;
    }

    public void addFragment (int index)
    {
        FragmentTransaction fragTrans = fM.beginTransaction();
        fragTrans.add (fragmentContainer.getId(), allFragments.get(index) );
        fragTrans.addToBackStack(null);
        fragTrans.commit();
    }

    public void switchTo (int index)
    {
        FragmentTransaction fragTrans = fM.beginTransaction();
        fragTrans.replace(fragmentContainer.getId(), allFragments.get(index));
        fragTrans.addToBackStack(null);
        fragTrans.commit();
    }
    public Fragment getCurrentFragment()
    {
        return fM.findFragmentById(R.id.fragment_container);

    }
}
