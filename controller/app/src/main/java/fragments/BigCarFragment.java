package fragments;

import android.app.Fragment;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.VideoView;

import joystick.JoystickHelper;
import com.controller.R;

import java.io.IOException;

/**
 * Created by Carl-Henrik Hult on 2016-03-23.
 */
public class BigCarFragment extends Fragment
{
    private ImageView logo;
    private VideoView big_video;
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

    }

    @Override
    public void onViewCreated(final View view, @Nullable Bundle savedInstanceState) {
        logo = (ImageView)getView().findViewById(R.id.big_logo);
        big_video = (VideoView)getView().findViewById(R.id.big_video);
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

    public void streamVideo(Uri uri, boolean start) {
        if(start) {
            big_video.setVideoURI(uri);
            big_video.start();
        } else {
            big_video.stopPlayback();
        }
    }



}
