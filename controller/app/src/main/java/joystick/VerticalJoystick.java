package joystick;

import android.app.Activity;
import android.content.Context;
import android.os.Vibrator;
import android.view.MotionEvent;
import android.widget.RelativeLayout;

import com.controller.MainActivity;
/**
 * Created by Carl-Henrik Hult on 2016-03-24.
 */
public class VerticalJoystick extends Joystick
{
    double minDistance = 0;
    MainActivity activity;
    public VerticalJoystick(Context context, RelativeLayout theLayout, double minDistance, Activity activity)
    {
        super(context, theLayout);
        if (minDistance >= 0)
        {
            this.minDistance = minDistance;
        }
        draw.position(params.width / 2, params.height / 2);
        draw();
        this.activity =(MainActivity) activity;
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
            if (!activity.getActivated())
            {
                draw.position(params.width / 2, params.height / 2);
                draw();
                /* Since this action means the joystick is released, it is no longer touched,
                 It gets reset */
                isTouched = false;
                position = 0;
            }
            else {
                isTouched = false;
            }
            Vibrator v = (Vibrator) this.context.getSystemService(Context.VIBRATOR_SERVICE);
            // Vibrate for 500 milliseconds

            long[] pattern = {0, 300, 100, 300};
            v.vibrate(pattern,-1);

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
