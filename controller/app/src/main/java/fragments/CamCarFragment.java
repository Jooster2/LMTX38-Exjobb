package fragments;

import android.app.Fragment;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.MediaPlayer;
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

import joystick.HorizontalJoystick;
import joystick.JoystickHelper;

import com.controller.MainActivity;
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

    private ImageView logo;
    private VideoView cam_video;
    private Uri uri;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.cam_car_fragment, container, false);

        JoystickHelper helper = new JoystickHelper(v, this);
        return v;
    }

    @Override
    public void onViewCreated(final View view, @Nullable Bundle savedInstanceState) {
        logo = (ImageView)getView().findViewById(R.id.cam_logo);
        cam_video = (VideoView)getView().findViewById(R.id.cam_video);
        cam_video.setOnErrorListener(new MediaPlayer.OnErrorListener() {
            @Override
            public boolean onError(MediaPlayer mp, int what, int extra) {
                cam_video.stopPlayback();
                cam_video.start();
                return true;
            }
        });
        cam_video.setOnInfoListener(new MediaPlayer.OnInfoListener() {
            @Override
            public boolean onInfo(MediaPlayer mp, int what, int extra) {
                if(what == MediaPlayer.MEDIA_INFO_BUFFERING_END) {
                    cam_video.resume();
                    Log.i("videoplayer", "resuming");
                    return true;
                } else if(what == MediaPlayer.MEDIA_INFO_BUFFERING_START) {
                    cam_video.pause();
                    Log.i("videoplayer", "pausing");
                    ((MainActivity)getActivity()).runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            ((MainActivity)getActivity()).resumeVideo(false);
                        }
                    });

                    return true;
                }
                return false;
            }
        });
    }

    public void cameraOn(boolean on) {
        if(on) {
            logo.setVisibility(View.INVISIBLE);
        } else {
            logo.setVisibility(View.VISIBLE);
        }
    }

    public void streamVideo(Uri uri, boolean start) {
        this.uri = uri;
        if(start) {
            cam_video.setVideoURI(uri);
            cam_video.start();
        } else {
            cam_video.stopPlayback();
        }
    }

    public void resumeVideo() {
        cam_video.resume();
    }
}
