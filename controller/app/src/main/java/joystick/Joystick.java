package joystick;

import android.content.Context;
import android.widget.RelativeLayout;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup.LayoutParams;

import com.controller.R;

import java.math.BigDecimal;
import java.math.RoundingMode;
/**
 * Created by Carl-Henrik Hult on 2016-03-24.
 */
public class Joystick
{
    private static final int NR_OF_DECIMALS = 2;

    Context context;
    RelativeLayout theLayout;
    DrawCanvas draw;
    Paint paint;
    LayoutParams params;

    // This is the joystick button that appears when pressed.
    Bitmap joystick;
    int joystick_width, joystick_height;

    double position = 0;
    boolean isTouched = false;
    boolean exceededMinDis = false;

    public Joystick (Context context, RelativeLayout theLayout)
    {
        this.context = context;
        this.theLayout = theLayout;
        draw = new DrawCanvas (context);
        paint = new Paint();

        //This will give hte width and height of the joystick pad
        params = theLayout.getLayoutParams();

        /*
        This fetches the image from res-folder, to rescale it and use it during run time.
        Unlike the "theLayout" viariable, that is a fixed view in a fragment, this is a
        dynamically drawn on image, that should only appear when joystick is pressed.
        */
        joystick = BitmapFactory.decodeResource(context.getResources(), R.drawable.joystick_pressed);
        joystick_height = params.height/4;
        joystick_width = params.width/4;
        joystick = Bitmap.createScaledBitmap(joystick, joystick_width, joystick_height,
                                             false);
        //*******************************************************************************
    }


    protected double getPosition()
    {
        BigDecimal bd = new BigDecimal(position);
        bd = bd.setScale(NR_OF_DECIMALS, RoundingMode.HALF_UP);
        position = bd.doubleValue();
        return position;
    }
    protected void draw()
    {
        /*
            First, remove old view, then add the view again, with new positioning.
         */
        theLayout.removeView(draw);
        theLayout.addView(draw);
    }

    public boolean checkInsideBoundries() {
        if(position >= -1 && position <= 1) {
            return true;
        }
        return false;
    }

    protected class DrawCanvas extends View
    {
        float x, y;

        private DrawCanvas(Context context) {
            super(context);
        }

        public void onDraw(Canvas canvas) {
            canvas.drawBitmap(joystick, x, y, paint);
        }

        public void position(float pos_x, float pos_y) {
            x = pos_x - (joystick_width / 2);
            y = pos_y - (joystick_height / 2);
        }
    }
}
