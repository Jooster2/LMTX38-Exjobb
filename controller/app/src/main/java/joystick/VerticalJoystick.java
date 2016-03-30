package joystick;

import android.content.Context;
import android.view.MotionEvent;
import android.widget.RelativeLayout;
/**
 * Created by Carl-Henrik Hult on 2016-03-24.
 */
public class VerticalJoystick extends Joystick
{
    double minDistance = 0;
    public VerticalJoystick(Context context, RelativeLayout theLayout, double minDistance)
    {
        super(context, theLayout);
        if (minDistance >= 0)
        {
            this.minDistance = minDistance;
        }
        draw.position(params.width/2, params.height/2);
        draw();
    }

    public void drawJoystick(MotionEvent event)
    {
        int action = event.getAction();
        position = (double) (event.getY() - params.width /2) / (params.width/2);

        if (action == MotionEvent.ACTION_DOWN)
        {
            draw.position(params.width/2, event.getY());
            draw();
            isTouched = true;
        }
        //If the finger travels over the joystick layout, a new image gets drawn.
        else if (action == MotionEvent.ACTION_MOVE && isTouched) {
            // If the action is outside of the joystick layout.
            if (checkInsideBoundries()) {
                draw.position(params.width / 2, event.getY());
                draw();
            }
            // If the action is made outside of the joystick layout.
            else {
                if (position < 0) {
                    position = -1;
                    draw.position(params.width/2, 0);
                    draw();
                } else if (position > 0) {
                    position = 1;
                    draw.position(params.width/2, params.height);
                    draw();
                }
            }
        }
        else if (action == MotionEvent.ACTION_UP)
        {
            draw.position(params.width / 2, params.height / 2);
            draw();
            /* Since this action means the joystick is released, it is no longer touched,
               It gets reset */
            isTouched = false;
            position = 0;
        }


    }

    /**
     * Gets the position of the drawn on image (which is also where the finger is) given that it is
     * far enough from the middle. How much is enough, is decided by the value on variable :minDistance
     * @return
     */
    public double getPosition()
    {
        if ((position > minDistance || position < (-1) * minDistance))
        {
            return super.getPosition();
        }
        return 0;
    }
}
