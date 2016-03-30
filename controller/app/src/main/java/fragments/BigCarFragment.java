package fragments;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import joystick.JoystickHelper;
import com.controller.R;
/**
 * Created by Carl-Henrik Hult on 2016-03-23.
 */
public class BigCarFragment extends Fragment
{
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.big_car_fragment, container, false);
        JoystickHelper helper = new JoystickHelper(v, this);
        return v;
    }
}
