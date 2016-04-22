package fragments;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RelativeLayout;

import joystick.HorizontalJoystick;
import joystick.JoystickHelper;
import com.controller.R;
import joystick.VerticalJoystick;
/**
 * Created by Carl-Henrik Hult on 2016-03-23.
 */
public class CamCarFragment extends Fragment
{

    RelativeLayout horizontal_joystick, vertical_joystick; // Background layout of the joystick (the pad or whatever)
    HorizontalJoystick h_joystick; // The actual joystick (smaller version that goes on top of the pad)
    VerticalJoystick v_joystick;
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.cam_car_fragment, container, false);

        JoystickHelper helper = new JoystickHelper(v, this);
        return v;
    }
}
