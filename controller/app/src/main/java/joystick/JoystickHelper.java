package joystick;

import android.app.Fragment;
import android.view.MotionEvent;
import android.view.View;
import android.widget.RelativeLayout;

import com.controller.R;
/**
 * Created by Carl-Henrik Hult on 2016-03-24.
 */
public class JoystickHelper
{

    RelativeLayout horizontal_joystick, vertical_joystick; // Background layout of the joystick (the pad or whatever)
    HorizontalJoystick h_joystick; // The actual joystick (smaller version that goes on top of the pad)
    VerticalJoystick v_joystick;

    public JoystickHelper (View view, Fragment client)
    {
        horizontal_joystick = (RelativeLayout)view.findViewById(R.id.horizontal_joystick);
        vertical_joystick = (RelativeLayout)view.findViewById(R.id.vertical_joystick);
        h_joystick = new HorizontalJoystick(client.getActivity().getApplicationContext(), horizontal_joystick, 0);
        v_joystick = new VerticalJoystick(client.getActivity().getApplicationContext(), vertical_joystick, 0.3);


        horizontal_joystick.setOnTouchListener(new View.OnTouchListener() {
            public boolean onTouch(View view, MotionEvent event) {
                h_joystick.drawJoystick(event);
                return true;
            }

        });
        vertical_joystick.setOnTouchListener(new View.OnTouchListener() {
            public boolean onTouch(View view, MotionEvent event) {
                v_joystick.drawJoystick(event);
                double temp = v_joystick.getPosition();
                if (temp < 0)
                    System.out.println("FORWARD: " + Math.abs(v_joystick.getPosition()));
                else
                    System.out.println("BACKWARD: "+v_joystick.getPosition());
                return true;
            }

        });

    }

}
