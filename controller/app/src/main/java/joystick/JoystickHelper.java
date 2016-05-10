package joystick;

import android.app.Fragment;
import android.view.MotionEvent;
import android.view.View;
import android.widget.RelativeLayout;

import com.controller.MainActivity;
import com.controller.R;
/**
 * Created by Carl-Henrik Hult on 2016-03-24.
 */
public class JoystickHelper
{

    RelativeLayout horizontal_joystick, vertical_joystick; // Background layout of the joystick (the pad or whatever)
    HorizontalJoystick h_joystick; // The actual joystick (smaller version that goes on top of the pad)
    VerticalJoystick v_joystick;
    double verticalLast = 0;
    double horizontalLast = 0;

    public JoystickHelper (View view, final Fragment client)
    {
        horizontal_joystick = (RelativeLayout)view.findViewById(R.id.horizontal_joystick);
        vertical_joystick = (RelativeLayout)view.findViewById(R.id.vertical_joystick);
        h_joystick = new HorizontalJoystick(client.getActivity().getApplicationContext(), horizontal_joystick, 0, client.getActivity() );
        v_joystick = new VerticalJoystick(client.getActivity().getApplicationContext(), vertical_joystick, 0, client.getActivity());

        horizontal_joystick.setOnTouchListener(new View.OnTouchListener() {
            public boolean onTouch(View view, MotionEvent event) {
                h_joystick.drawJoystick(event);
                MainActivity act = (MainActivity)client.getActivity();
                double temp = h_joystick.getPosition();
                if(temp != horizontalLast) {
                    act.sendToCar("HORIZONTAL", temp);
                    horizontalLast = temp;
                }
                if ((event.getAction() ==  event.ACTION_UP)&& !act.getActivated() )
                {
                    act.sendToCar("HORIZONTAL", 0);
                }
                return true;
            }

        });
        vertical_joystick.setOnTouchListener(new View.OnTouchListener() {
            public boolean onTouch(View view, MotionEvent event) {
                v_joystick.drawJoystick(event);
                MainActivity act = (MainActivity)client.getActivity();
                double temp = v_joystick.getPosition();
                if(temp != verticalLast)
                {
                    act.sendToCar("VERTICAL", temp);
                    verticalLast = temp;
                }
                if ((event.getAction() ==  event.ACTION_UP)&& !act.getActivated() )
                {
                    act.sendToCar("VERTICAL", 0);
                }
                return true;
            }

        });

    }

}
