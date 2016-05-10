package fragments;

import android.app.Fragment;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;

import joystick.JoystickHelper;
import com.controller.R;
/**
 * Created by Carl-Henrik Hult on 2016-03-23.
 */
public class BigCarFragment extends Fragment
{
    private ImageView logo;
    private RelativeLayout bground;
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        logo = (ImageView)getView().findViewById(R.id.big_logo);
        bground = (RelativeLayout)getView().findViewById(R.id.big_bground);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.big_car_fragment, container, false);
        JoystickHelper helper = new JoystickHelper(v, this);
        return v;
    }

    public void cameraOn(boolean on) {
        if(on) {
            logo.setVisibility(View.INVISIBLE);
        } else {
            logo.setVisibility(View.VISIBLE);
        }
    }

    public void setBground(BitmapDrawable image) {
        bground.setBackground(image);
    }

}
