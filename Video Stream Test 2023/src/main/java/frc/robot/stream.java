package frc.robot;
import java.util.Map;

import edu.wpi.first.cameraserver.CameraServer;
import edu.wpi.first.cscore.MjpegServer;
import edu.wpi.first.cscore.UsbCamera;
import edu.wpi.first.cscore.VideoSink;
import edu.wpi.first.cscore.VideoSource;
import edu.wpi.first.wpilibj.shuffleboard.ComplexWidget;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;

/**
 * A `VideoSource` that toggles between a front and back camera.
 */
public class stream{
    private final UsbCamera top;
    //private final UsbCamera bottom;

    private static final int TOP_EXPOSURE = 39;
    private static final int TOP_BRIGHTNESS = 5;

    private static final int BOTTOM_EXPOSURE = 39;
    private static final int BOTTOM_BRIGHTNESS = 5;

    private final VideoSink server;

    private boolean topActive = true;
    public stream() {
        top = CameraServer.startAutomaticCapture(0);
        top.setResolution(200, 100);
        top.setExposureManual(TOP_EXPOSURE);
        top.setBrightness(TOP_BRIGHTNESS);
        top.setFPS(60);
        server = CameraServer.getServer();
        server.setSource(top);
        /*
        top = new UsbCamera("0", 0);
        MjpegServer mjpegServer1 = new MjpegServer("s0", 1181);
        mjpegServer1.setSource(top);
        */
        /*
        bottom = CameraServer.startAutomaticCapture();
        bottom.setResolution(140, 120);
        bottom.setExposureManual(BOTTOM_EXPOSURE);
        bottom.setBrightness(BOTTOM_BRIGHTNESS);
        bottom.setFPS(30);
        */

    }
}